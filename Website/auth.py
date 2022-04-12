
from pickle import TRUE
from flask import render_template, url_for, request, Blueprint, flash, redirect, session
from sqlalchemy import null, true
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user
import graphADT
from . import db
from .models import User, drivertble
from oneMapMethods import locationdet
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
    return render_template('login.html')


@auth.route('/', methods=['GET', 'POST'])
def login_post():
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
    return redirect(url_for('auth.home'))


# Route to driver page
@auth.route('/driver')
def driverLogin():
    return render_template("driver.html")


@auth.route('/driver', methods=['GET', 'POST'])
def driverLogin_post():
    username = request.form.get('username')
    password = request.form.get('password')
    driver = drivertble.query.filter_by(username=username).first()
    session['driverAvailable'] = driver.isAvailable
    available = session['driverAvailable']
    session['driverID'] = driver.id
    session['driverUsername'] = username
    if available == 'TRUE': # if driver isavailable
        return redirect(url_for('auth.driverHome')) # redirect to location of curr driver
    if available == 'FALSE':
        return redirect(url_for('auth.driverHome'))
    session['driverPath'] = driver.journeyRoute
    print(driver.journeyRoute)
    
    if not driver or not driver.password:
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.driverLogin'))
    # if driver exists, log driver in
    login_user(driver, remember=True)
    return redirect(url_for('auth.driverRoute'))

# driver log in
    # newDriver = Driver(driverName) # get from DB
    # if driver start job:
    # newDriver.startJob(start) # get from webpage start loc as ID (1,2,3...), Update Web Page with driverLoc
    # end

# driver log in if not avail
#     newDriver = Driver(driverName, driverStart)

# don't have to run this part if we can store driver nodes in webpage global array
#     driverPath, driverDistance = newDriver.driverRoute(driverLoc, customerLoc) get from DB driverLoc, customerLoc
#     print('your route is', driverPath, 'your customer is at', customerLoc, your distance is, driverDistance)


# Route to driver homepage
@auth.route('/driverHome', methods=['GET', 'POST'])
@login_required
def driverHome():
    driverUsername = session['driverUsername']
    # ridePath = session['ridePath']
    # print('ride path is', ridePath)
    # print(ridePath[0])
    if request.method == 'POST':
        isAvailable = request.form.get('isAvailable')
        driverloc = request.form.get('startLoc')

        drivertble.query.filter(drivertble.username == driverUsername).update({'driverloc': driverloc})
        drivertble.query.filter(drivertble.username == driverUsername).update({'isAvailable': isAvailable})
        db.session.commit()
        
        return redirect(url_for('auth.driverLocation',startLoc=driverloc))

    return render_template("driverHome.html")


@auth.route('/driverRoute', methods=['GET', 'POST'])
@login_required
def driverRoute():
    if request.method == 'POST':
        return redirect(url_for("auth.driverLogin"))

    driverPath = session['driverPath']
    print(driverPath)
    driverPath=driverPath.replace('[', '')
    driverPath=driverPath.replace(']', '')
    driverPath=driverPath.replace(',', '')
    driverPath = driverPath.split(' ')
    print(driverPath)
    graph = graphADT.g
    path = []
    for i in driverPath:
        if i != '':
            if int(i) in graph.locations:
                path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
    print(path)
    print(type(path))
    for i in range(0,len(path)):
        if path[i] == path[i-1]:
            temp = path[i]
    print(temp)
    m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)
    plugins.AntPath(
        locations=path
    ).add_to(m)
    folium.Marker(
        location=path[0],
        icon=folium.Icon(color="green", icon="map-marker"), tooltip="Your Location"
    ).add_to(m)
    folium.Marker(
        location=temp,
        icon=folium.Icon(color="red", icon="map-marker"), tooltip="Customer Location"
    ).add_to(m)
    folium.Marker(
        location=path[-1],
        icon=folium.Icon(color="blue", icon="map-marker"), tooltip="Customer Destination"
    ).add_to(m)
    m.fit_bounds([path[0], path[-1]])

    return render_template("driverRoute.html", map=m._repr_html_(), driverStatus='Driver is on the way')


# Route to driver location
@auth.route('/driverLocation', methods=['GET', 'POST'])
@login_required
def driverLocation():
    driverUsername = session['driverUsername']
    driverID = session['driverID']
    startLoc = request.args.get('startLoc')

    Driver(driverUsername, driverID)

    return render_template("driverLocation.html")


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

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email, onRide="", journeyRoute="")
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


# Route to book ride page
@auth.route('/bookride', methods=['GET', 'POST'])
@login_required
def bookride():
    if request.method == 'POST':
        start = request.form.get('pickUp')
        end = request.form.get('dropOff')
        maxDist = request.form.get('searchRange')

        return redirect(url_for('auth.confirmride',startPoint=start,endPoint=end,maxDist=maxDist))

    return render_template("bookride.html")


@auth.route('/confirmride', methods=['GET', 'POST'])
@login_required
def confirmride():
    graph = graphADT.g
    getDriver = drivertble.query.all()
    for driver in getDriver:
        graph.drivers.update({int(driver.id): [driver.username,driver.carplate]})
        if(driver.isAvailable.lower() == 'true'):
            if int(driver.driverloc) not in graph.driverLocation:
                graph.driverLocation.update({int(driver.driverloc): [int(driver.id)]})
            elif (int(driver.id) not in graph.driverLocation[int(driver.driverloc)]):
                graph.driverLocation[int(driver.driverloc)].append(int(driver.id))

    baseFare = 4.05  # taken from comfortdelgo website
    perKMPrice = 0.7  # taken from comfortdelgo website
    newCustomer = customer.Customer(session.get('customerName', None))
    start = request.args.get('startPoint', None)
    end = request.args.get('endPoint', None)
    maxDist = request.args.get('maxDist', None)
    customerPath, customerDistance = newCustomer.getCustomerRide(start, end)  # get from DB
    session['customerStart']=start
    session['customerEnd']=end
    path = []
    for i in customerPath:
        if i in graph.locations:
            path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
    session['customerPath']=customerPath
    startLocation = (graph.locations[int(start)][0])
    endLocation = (graph.locations[int(end)][0])

    rideCost = baseFare + customerDistance * perKMPrice
    rideCost = round(rideCost, 2)
    customerDistance = round(customerDistance, 2)
    m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)
        # folium.PolyLine(
        #     locations=path
        # ).add_to(m)

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

    if request.method == 'POST':
        return redirect(url_for('auth.rideDetails',customerDistance=customerDistance, startLocation=startLocation,
    endLocation=endLocation, maxDist=maxDist, rideCost=rideCost))

    return render_template("confirmride.html", map=m._repr_html_(),customerDistance=customerDistance, startLocation=startLocation,
    endLocation=endLocation, rideCost=rideCost)


@auth.route('/rideDetails', methods=['GET','POST'])
@login_required
def rideDetails():
    if request.method == 'POST':
        return redirect(url_for("auth.home"))

    startLocation = request.args.get('startLocation', None)
    endLocation = request.args.get('endLocation', None)
    customerDistance = request.args.get('customerDistance', None)
    maxDist = request.args.get('maxDist', None)
    rideCost = request.args.get('rideCost', None)
    if maxDist =="noPref":
        maxDist=99999999
    graph = graphADT.g
    customerName = session['customerName']
    start = session['customerStart']
    end = session['customerEnd']
    booking = NewBooking(int(start), float(maxDist), customerName)
    driverStart, driverID, driverName = booking.finddriver()

    if driverStart != 'No driver':
        customerPath = session['customerPath']
        driverInfo = 'Your Driver is: ' + driverName
        drivertble.query.filter(drivertble.id == int(driverID)).update({'driverloc': int(end)})
        if int(driverStart) != int(start):
            # update driverID in DB isAvailable to not True, set current customer to = CustomerName, CustomerLoc = Start
            newDriver = Driver(driverName, driverStart)
            driverPath, driverDistance = newDriver.driverRoute(driverStart, int(start))
            totalPath = np.concatenate((driverPath,customerPath))

            path = []
            for i in driverPath:
                if i in graph.locations:
                    path.append([graph.locations[int(i)][1], graph.locations[int(i)][2]])
            startLocation = (graph.locations[int(start)][0])
            endLocation = (graph.locations[int(end)][0])
            driverLocation = (graph.locations[driverStart][0])

            m = folium.Map(location=[1.3541, 103.8198], tiles='OpenStreetMap', zoom_start=12, control_scale=True)

            plugins.AntPath(
                locations=path
            ).add_to(m)
            folium.Marker(
                location=path[0],
                icon = folium.Icon(color="green", icon="map-marker"),
                popup=driverLocation, tooltip="Your Driver's Location"
            ).add_to(m)
            folium.Marker(
                location=path[-1],
                icon = folium.Icon(color="blue", icon="map-marker"),
                popup = endLocation, tooltip = "Your Location"
            ).add_to(m)
            m.fit_bounds([path[0], path[-1]])
            db.session.query(drivertble).filter(drivertble.username == driverName).update({'journeyRoute': str(totalPath)}) # driverPath
            db.session.query(drivertble).filter(drivertble.username == driverName).update({'isAvailable': 'DRIVING'})
            db.session.commit()
        else:  # driver at current location
            path = []
            path.append([graph.locations[int(start)][1], graph.locations[int(start)][2]])
            m = folium.Map(location=path[0], tiles='OpenStreetMap', zoom_start=18, control_scale=True)
            folium.Marker(
                location=path[0],
                icon = folium.Icon(color="green", icon="map-marker"),
                popup=startLocation, tooltip="Your Location"
            ).add_to(m)
            print(customerPath)
            customerPath.insert(0,int(start))
            print(customerPath)
            totalPath = customerPath
            print(totalPath)
            # totalPath = np.concatenate((driverPath,customerPath))
            db.session.query(drivertble).filter(drivertble.username == driverName).update({'journeyRoute': str(totalPath)}) # driverPath
            db.session.query(drivertble).filter(drivertble.username == driverName).update({'isAvailable': 'DRIVING'})
            db.session.commit()
            return render_template("rideDetails.html", map=m._repr_html_(), customerDistance=customerDistance,
                                   startLocation=startLocation,
                                   endLocation=endLocation, rideCost=rideCost, driverInfo=driverInfo,
                                   driverStatus='Driver has arrived!')
        return render_template("rideDetails.html", map=m._repr_html_(),customerDistance=customerDistance, startLocation=startLocation,
                                endLocation=endLocation,rideCost=rideCost, driverInfo=driverInfo, driverStatus='Driver is on the way')
    else: # no driver available
        return render_template("rideisHere.html", customerDistance=customerDistance, startLocation=startLocation,
                                endLocation=endLocation, rideCost=rideCost, driverStatus=driverStart)

