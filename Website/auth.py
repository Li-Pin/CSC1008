
from flask import render_template, url_for, request, Blueprint, flash, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user, logout_user
from graphADT import g as graph
from . import db
from .models import User, drivertble
import customer
from driver import Driver
import folium
from folium import plugins
from matching import NewBooking
import numpy as np

auth = Blueprint('auth', __name__)


# Route to login page
@auth.route('/')
def login():
    session['databaseValue'] = 1
    return render_template('login.html')


@auth.route('/', methods=['GET', 'POST'])
def login_post():
    session['databaseValue'] = 1
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.filter_by(username=username).first()

    # check if user exists
    # if user don't exist, prompt user to try again
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.login'))
    # if user exists, log user in
    login_user(user, remember=True)
    session['customerName'] = username

    if user.onRide == 'TRUE':
        return redirect(url_for('auth.customerRoute'))
    return redirect(url_for('auth.home'))


@auth.route('/customerRoute', methods=['GET', 'POST'])
@login_required
def customerRoute():
    username = session['customerName']
    user = User.query.filter_by(username=username).first()
    session['userPath'] = user.journeyRoute
    if request.method == 'POST':
        if request.form['submit_button'] == 'logout':
            logout_user()
            return redirect(url_for("auth.login"))
        elif request.form['submit_button'] == 'completeTrip':
            username = session['customerName']
            db.session.query(User).filter(User.username == username).update({'onRide': 'FALSE'})
            db.session.commit()
            return redirect(url_for("auth.home"))
    customerPath = session['userPath']
    customerPath = customerPath.replace('[', '')
    customerPath = customerPath.replace(']', '')
    customerPath = customerPath.replace(',', '')
    customerPath = customerPath.replace('', '')
    customerPath = customerPath.split(' ')
    path = []
    for i in customerPath:
        if i != '':
            if int(i) in graph.locations:
                path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
    for i in customerPath:
        if i != '':
            startindex = i
            break
    for i in range(0, len(path)):
        if path[i] == path[i - 1]:
            temp = path[i]
    endindex = customerPath[-1]
    startLocation = (graph.locations[int(startindex)][0])
    endLocation = (graph.locations[int(endindex)][0])
    m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)
    plugins.AntPath(
        locations=path
    ).add_to(m)
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color="green", icon="map-marker"), tooltip="Driver Location", popup=startLocation
    ).add_to(m)
    folium.Marker(
        location=temp,
        icon=folium.Icon(color="red", icon="map-marker"), tooltip="Your Location"
    ).add_to(m)
    folium.Marker(
        location=path[-1],
        icon=folium.Icon(color="blue", icon="map-marker"), tooltip="Your Destination", popup=endLocation
    ).add_to(m)
    m.fit_bounds([path[0], path[-1]])

    return render_template("customerRoute.html", map=m._repr_html_(), driverStatus='Waiting for Driver',
                           startLocation=startLocation, endLocation=endLocation)


# Route to driver page
@auth.route('/driver')
def driverLogin():
    session['databaseValue'] = 2
    return render_template("driver.html")


@auth.route('/driver', methods=['GET', 'POST'])
def driverLogin_post():
    session['databaseValue'] = 2
    if request.method == 'POST':
        if request.form['submit_button'] == 'login':
            username = request.form.get('username')
            password = request.form.get('password')
            driver = drivertble.query.filter_by(username=username).first()  # getting driver details
            if not driver or password != driver.password:
                flash('Please check your login details and try again.', 'danger')
                return redirect(url_for('auth.driverLogin'))
            # if driver exists, log driver in
            else:
                login_user(driver, remember=True)
                session['driverAvailable'] = driver.isAvailable  # setting driver availability
                available = session['driverAvailable']
                # setting session variables
                session['driverUsername'] = username
                session['driverID'] = driver.id
                if available == 'TRUE':  # if driver working but not on job
                    session['driverloc'] = driver.driverloc
                    return redirect(url_for('auth.driverLocation'))  # redirect to location of curr driver

                elif available == 'DRIVING':  # if driver not working
                    session['driverPath'] = driver.journeyRoute
                    return redirect(url_for('auth.driverRoute'))
                else:
                    return redirect(url_for('auth.driverHome'))
        elif request.form['submit_button'] == 'back':
            return redirect(url_for('auth.login'))

# Route to driver homepage
@auth.route('/driverHome', methods=['GET', 'POST'])
@login_required
def driverHome():
    driverUsername = session['driverUsername']
    m = folium.Map(location=[1.3541, 103.8198], width='100%', height=500, tiles='OpenStreetMap', zoom_start=12,
                   control_scale=True)
    locarr = []
    for loc in graph.locations:
        locarr.append([graph.locations[int(loc)][1], graph.locations[int(loc)][2]])
    for i in range(0, len(locarr)):
        locationName = (graph.locations[i][0])
        folium.Marker(
            location=locarr[i],
            icon=folium.Icon(color="blue", icon="map-marker"), tooltip=locationName
        ).add_to(m)
    m.fit_bounds([locarr[0], locarr[-1]])

    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            isAvailable = request.form.get('isAvailable')
            if isAvailable == 'TRUE':
                driverloc = request.form.get('startLoc')
                session['driverloc'] = driverloc
                db.session.query(drivertble).filter(drivertble.username == driverUsername).update(
                    {'driverloc': driverloc})
                db.session.query(drivertble).filter(drivertble.username == driverUsername).update(
                    {'isAvailable': isAvailable})
                db.session.commit()
                return redirect(url_for('auth.driverLocation', startLoc=driverloc))
            else: # here is driver
                driverLoc = session['driverloc']
                index = 0
                for i in graph.driverLocation:
                    if i == int(driverLoc):
                        for j in graph.driverLocation[i]:
                            driverID = session['driverID']
                            if j == driverID:
                                graph.driverLocation[i].pop(index)
                                break
                            index += 1
                driverloc = ''
                db.session.query(drivertble).filter(drivertble.username == driverUsername).update(
                    {'driverloc': driverloc})
                db.session.query(drivertble).filter(drivertble.username == driverUsername).update(
                    {'isAvailable': isAvailable})
                db.session.commit()


        elif request.form['submit_button'] == 'logout':
            logout_user()
            return redirect(url_for('auth.driverLogin'))

    return render_template("driverHome.html", map=m._repr_html_())


@auth.route('/driverRoute', methods=['GET', 'POST'])
@login_required
def driverRoute():
    driverUsername = session['driverUsername']
    if request.method == 'POST':
        if request.form['submit_button'] == 'logout':
            logout_user()
            return redirect(url_for("auth.driverLogin"))
        elif request.form['submit_button'] == 'completeTrip':
            db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'isAvailable': 'TRUE'})
            db.session.commit()
            return redirect(url_for("auth.driverHome"))
    driverPath = session['driverPath']
    driverPath = driverPath.replace('[', '')
    driverPath = driverPath.replace(']', '')
    driverPath = driverPath.replace(',', '')
    driverPath = driverPath.replace('', '')
    driverPath = driverPath.split(' ')

    path = []
    for i in driverPath:
        if i != '':
            if int(i) in graph.locations:
                path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
    for i in driverPath:
        if i != '':
            startindex = i
            break
    for i in range(0, len(path)):
        if path[i] == path[i - 1]:
            temp = path[i]
    endindex = driverPath[-1]
    startLocation = (graph.locations[int(startindex)][0])
    endLocation = (graph.locations[int(endindex)][0])
    m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)
    plugins.AntPath(
        locations=path
    ).add_to(m)
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color="green", icon="map-marker"), tooltip="Your Location", popup=startLocation
    ).add_to(m)
    folium.Marker(
        location=temp,
        icon=folium.Icon(color="red", icon="map-marker"), tooltip="Customer Location"
    ).add_to(m)
    folium.Marker(
        location=path[-1],
        icon=folium.Icon(color="blue", icon="map-marker"), tooltip="Customer Destination", popup=endLocation
    ).add_to(m)
    m.fit_bounds([path[0], path[-1]])

    return render_template("driverRoute.html", map=m._repr_html_(), driverStatus='Get to your customer',
                           startLocation=startLocation, endLocation=endLocation)


# Route to driver location
@auth.route('/driverLocation', methods=['GET', 'POST'])
@login_required
def driverLocation():
    driverUsername = session['driverUsername']
    driverID = session['driverID']
    driverAt = session['driverloc']
    startLocation = (graph.locations[int(driverAt)][0])
    path = []
    path.append([graph.locations[int(driverAt)][1], graph.locations[int(driverAt)][2]])
    m = folium.Map(location=path[0], tiles='OpenStreetMap', zoom_start=18, control_scale=True)
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color="green", icon="map-marker"),
        popup=startLocation, tooltip="Your Location"
    ).add_to(m)
    Driver(driverUsername, driverID)
    if request.method == 'POST':
        if request.form['submit_button'] == 'endShift':
            driverLoc = session['driverloc']
            index = 0
            for i in graph.driverLocation:
                if i == int(driverLoc):
                    for j in graph.driverLocation[i]:
                        driverID = session['driverID']
                        if j == driverID:
                            graph.driverLocation[i].pop(index)
                            break
                        index += 1
            db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'driverloc': ''})
            db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'isAvailable': 'FALSE'})
            db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'journeyRoute': ''})
            db.session.commit()
            return redirect(url_for("auth.driverHome"))
        elif request.form['submit_button'] == 'home':
            return redirect(url_for("auth.driverHome"))
    return render_template("driverLocation.html", map=m._repr_html_(), driverUsername=driverUsername,
                           startLocation=startLocation)


# Route to register page
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')

        # if it returns a user, there is already an existing user with the same email
        user = User.query.filter_by(email=email).first()

        # if there is an existing user, prompt user to try again
        if user:
            flash('Email address already exist, please use another email.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email,
                        onRide="", journeyRoute="")
        db.session.add(new_user)
        db.session.commit()
        # login_user(user, remember=True)
        flash('Registration Success!', 'success')
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# Route to homepage
@auth.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    username = session['customerName']
    return render_template("home.html", username=username)


# Route to homepage if ride is booked
@auth.route('/homebooked', methods=['GET', 'POST'])
@login_required
def homebooked():
    username = session['customerName']
    return render_template("homebooked.html", username=username)


# Route to book ride page
@auth.route('/bookride', methods=['GET', 'POST'])
@login_required
def bookride():
    getDriver = drivertble.query.all()
    for driver in getDriver:
        graph.drivers.update({int(driver.id): [driver.username, driver.carplate]})
        if driver.isAvailable.lower() == 'true' and driver.driverloc is not None:
            if int(driver.driverloc) not in graph.driverLocation:
                graph.driverLocation.update({int(driver.driverloc): [int(driver.id)]})
            elif int(driver.id) not in graph.driverLocation[int(driver.driverloc)]:
                graph.driverLocation[int(driver.driverloc)].append(int(driver.id))

    m = folium.Map(location=[1.3541, 103.8198], width='100%', height='100%', tiles='OpenStreetMap', zoom_start=12,
                   control_scale=True)
    locarr = []
    for loc in graph.locations:
        locarr.append([graph.locations[int(loc)][1], graph.locations[int(loc)][2]])
    for i in range(0, len(locarr)):
        locationName = (graph.locations[i][0])
        folium.Marker(
            location=locarr[i],
            icon=folium.Icon(color="blue", icon="map-marker"), tooltip=locationName
        ).add_to(m)
    m.fit_bounds([locarr[0], locarr[-1]])
    # Plotting of driver locations on map
    driverarr = []
    for drivers in graph.driverLocation:
        if len(graph.driverLocation[drivers])>0:
            driverarr.append([graph.locations[int(drivers)][1], graph.locations[int(drivers)][2]])
    for i in range(0, len(driverarr)):
        folium.Marker(
            location=driverarr[i],
            icon=folium.Icon(color="green", icon="map-marker"), tooltip="Driver here!"
        ).add_to(m)
    m.fit_bounds([locarr[0], locarr[-1]])

    if request.method == 'POST':
        start = request.form.get('pickUp')
        end = request.form.get('dropOff')
        if start == end:
            flash('Your start and end location are the same!', 'danger')
            return redirect(url_for('auth.bookride'))
        return redirect(url_for('auth.confirmride',startPoint=start,endPoint=end))
    return render_template("bookride.html",map=m._repr_html_())


@auth.route('/confirmride', methods=['GET', 'POST'])
@login_required
def confirmride():
    # Declaring constant variable for calculations
    baseFare = 4.05  # taken from comfortdelgo website
    perKMPrice = 0.7  # taken from comfortdelgo website
    # Intialising new customer class
    newCustomer = customer.Customer(session.get('customerName', None))
    start = request.args.get('startPoint', None)
    end = request.args.get('endPoint', None)
    customerPath, customerDistance = newCustomer.getCustomerRide(start, end)  # get from DB
    session['customerStart'] = start
    session['customerEnd'] = end
    path = []
    # Setting path for map to draw route
    for i in customerPath:
        if i in graph.locations:
            path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
    session['customerPath'] = customerPath
    startLocation = (graph.locations[int(start)][0])
    endLocation = (graph.locations[int(end)][0])
    # Calculating ride cost based on ComfortDelgro website
    rideCost = baseFare + customerDistance * perKMPrice
    rideCost = round(rideCost, 2)
    customerDistance = round(customerDistance, 2)
    # Initialising Map
    m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)
    # Plotting of map
    plugins.AntPath(
        locations=path
    ).add_to(m)
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color="blue", icon="map-marker"),
        popup=startLocation, tooltip="Your Location"
    ).add_to(m)
    folium.Marker(
        location=path[-1],
        icon=folium.Icon(color="red", icon="map-marker"),
        popup=endLocation, tooltip="Your Destination"
    ).add_to(m)
    m.fit_bounds([path[0], path[-1]])

    # Redirect to rideDetails with ride information
    if request.method == 'POST':
        return redirect(url_for('auth.rideDetails', customerDistance=customerDistance, startLocation=startLocation,
                                endLocation=endLocation, rideCost=rideCost))

    return render_template("confirmride.html", map=m._repr_html_(), customerDistance=customerDistance,
                           startLocation=startLocation,
                           endLocation=endLocation, rideCost=rideCost)


@auth.route('/rideDetails', methods=['GET', 'POST'])
@login_required
def rideDetails():
    if request.method == 'POST':
        onRide = session['onRide']
        # if user already has a ride, redirect to show current ride (homebooked.html)
        if onRide == 'TRUE':
            return redirect(url_for("auth.homebooked"))

        return redirect(url_for("auth.home"))

    # getting variables from previous function
    startLocation = request.args.get('startLocation', None)
    endLocation = request.args.get('endLocation', None)
    customerDistance = request.args.get('customerDistance', None)
    rideCost = request.args.get('rideCost', None)
    # getting variables from respective session variables
    customerName = session['customerName']
    start = session['customerStart']
    end = session['customerEnd']
    # initialise new booking to match driver and customer
    booking = NewBooking(int(start), customerName)
    driverStart, driverID, driverName = booking.finddriver()
    # if there is driver
    if driverStart != 'No driver':
        # Update customerPath with session customerPath
        customerPath = session['customerPath']
        # driverInfo to be passed to html
        driverInfo = 'Your Driver is: ' + driverName
        # getting data from database
        drivertble.query.filter(drivertble.id == int(driverID)).update({'driverloc': int(end)})
        # if driver and passenger are not at the same location
        if int(driverStart) != int(start):
            # update driverID in DB isAvailable to not True, set current customer to = CustomerName, CustomerLoc = Start
            newDriver = Driver(driverName, driverStart)
            driverPath, driverDistance = newDriver.driverRoute(driverStart, int(start))
            totalPath = np.concatenate((driverPath, customerPath))
            path = []
            for i in driverPath:
                if i in graph.locations:
                    path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
            startLocation = (graph.locations[int(start)][0])
            endLocation = (graph.locations[int(end)][0])
            driverLocation = (graph.locations[driverStart][0])

            # Initialising Map
            m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)

            # Drawing path route
            plugins.AntPath(
                locations=path
            ).add_to(m)
            folium.Marker(
                location=path[0],
                icon=folium.Icon(color="green", icon="map-marker"),
                popup=driverLocation, tooltip="Your Driver's Location"
            ).add_to(m)

            # Adding user location to map
            folium.Marker(
                location=path[-1],
                icon=folium.Icon(color="blue", icon="map-marker"),
                popup=endLocation, tooltip="Your Location"
            ).add_to(m)
            m.fit_bounds([path[0], path[-1]])
            updateDB(driverName, totalPath, customerName)
        # driver at current location
        else:
            # initialising array to store path coordinates
            path = []
            path.append([graph.locations[int(start)][1], graph.locations[int(start)][2]])
            # initialising map
            m = folium.Map(location=path[0], tiles='OpenStreetMap', zoom_start=18, control_scale=True)
            # Adding user location to map
            folium.Marker(
                location=path[0],
                icon=folium.Icon(color="green", icon="map-marker"),
                popup=startLocation, tooltip="Your Location"
            ).add_to(m)
            # Inserting customer start to path array for plotting of customer location in total path
            customerPath.insert(0, int(start))
            # Assigning customerPath to totalPath
            totalPath = customerPath
            updateDB(driverName, totalPath, customerName)
            return render_template("rideDetails.html", map=m._repr_html_(), customerDistance=customerDistance,
                                   startLocation=startLocation,
                                   endLocation=endLocation, rideCost=rideCost, driverInfo=driverInfo,
                                   driverStatus='Driver has arrived!')
        return render_template("rideDetails.html", map=m._repr_html_(), customerDistance=customerDistance,
                               startLocation=startLocation,
                               endLocation=endLocation, rideCost=rideCost, driverInfo=driverInfo,
                               driverStatus='Driver is on the way')
    # no driver available
    else:
        return render_template("noRide.html", customerDistance=customerDistance, startLocation=startLocation,
                               endLocation=endLocation, rideCost=rideCost, driverStatus=driverStart)


#  Setting driver availability to 'DRIVING', upload customer journey path and setting onRide to true
def updateDB(driverName, totalPath, customerName):
    db.session.query(drivertble).filter(drivertble.username == driverName).update(
        {'journeyRoute': str(totalPath)})
    db.session.query(drivertble).filter(drivertble.username == driverName).update({'isAvailable': 'DRIVING'})
    db.session.query(User).filter(User.username == customerName).update({'journeyRoute': str(totalPath)})
    db.session.query(User).filter(User.username == customerName).update({'onRide': 'TRUE'})
    session['onRide'] = 'TRUE'
    db.session.commit()
