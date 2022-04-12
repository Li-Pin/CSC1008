
from pickle import TRUE
from flask import render_template, url_for, request, Blueprint, flash, redirect, session
from sqlalchemy import null, true
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, current_user
import graphADT
from . import db
from .models import User, TEST_ride2, TEST_shared, drivertble
from oneMapMethods import locationdet
import customer
from driver import Driver
import folium
from folium import plugins
from matching import NewBooking

auth = Blueprint('auth', __name__)

customerPath = []
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
    session['driverID'] = driver.id
    session['driverUsername'] = username
    # check if driver exists
    # if driver don't exist, prompt driver to try again
    if not driver or not driver.password:
        flash('Please check your login details and try again.', 'danger')
        return redirect(url_for('auth.driverLogin'))
    # if driver exists, log driver in
    login_user(driver, remember=True)
    return redirect(url_for('auth.driverHome'))

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
    if request.method == 'POST':
        isAvailable = request.form.get('isAvailable')
        driverloc = request.form.get('startLoc')

        db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'driverloc': driverloc})
        db.session.query(drivertble).filter(drivertble.username == driverUsername).update({'isAvailable': isAvailable})
        db.session.commit()

        return redirect(url_for('auth.driverLocation',startLoc=driverloc))

    return render_template("driverHome.html")


# Route to driver location
@auth.route('/driverLocation', methods=['GET', 'POST'])
@login_required
def driverLocation():
    driverUsername = session['driverUsername']
    driverID = session['driverID']
    startLoc = request.args.get('startLoc')
    driver = Driver(driverUsername, driverID)
    #driver.startjob(startLoc)

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

        new_user = User(username=username, password=generate_password_hash(password, method='sha256'), email=email)
        db.session.add(new_user)
        db.session.commit()
        login_user(user, remember=True)
        flash('Registration Success!', 'success')
        return redirect(url_for("auth.login"))

    return render_template("register.html")


# Route to homepage
@auth.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html")


# Route to book ride page
@auth.route('/bookride', methods=['GET', 'POST'])
@login_required
def bookride():
    if request.method == 'POST':
        start = request.form.get('pickUp')  # to replace with form.get.(=start)
        end = request.form.get('dropOff')  # to replace with form.get.(=end)
        maxDist = request.form.get('searchRange')

        return redirect(url_for('auth.confirmride',startPoint=start,endPoint=end,maxDist=maxDist))

    return render_template("bookride.html")


# Route to book shared ride page
@auth.route('/booksharedride', methods=['GET', 'POST'])
@login_required
def booksharedride():
    if request.method == 'POST':
        pickUp = request.form.get('pickUp')  # Taking input from form
        dropOff = request.form.get('dropOff')
        time = request.form.get('time')
        pax = request.form.get('pax')
        carType = request.form.get('carType')
        date = request.form.get('date')
        paym = request.form.get('paym')

        fromLocation = locationdet(pickUp)  # Passing to API
        toLocation = locationdet(dropOff)
        fromLocationlat = fromLocation[0]  # Assigning array values
        fromLocationlong = fromLocation[1]
        toLocationlat = toLocation[0]
        toLocationlong = toLocation[1]
        fromLocationname = fromLocation[2]
        toLocationname = toLocation[2]

        Share_Ride = TEST_shared(pickUp=pickUp, carType=carType, dropOff=dropOff, pax=pax, date=date, time=time,
                                 paym=paym)
        db.session.add(Share_Ride)
        db.session.commit()
        return redirect(url_for('auth.confirmride', fromLocationlat=fromLocationlat, fromLocationlong=fromLocationlong,
                                toLocationlat=toLocationlat, toLocationlong=toLocationlong,
                                fromLocationname=fromLocationname, toLocationname=toLocationname))
        return redirect(url_for("auth.confirmride"))
    return render_template("booksharedride.html")


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
        drivertble.query.filter(drivertble.id == int(driverID)).update({'driverloc': int(end)})
        drivertble.query.filter(drivertble.id == int(driverID)).update({'isAvailable': 'FALSE'})
        db.session.commit()
        driverInfo = 'Your Driver is: ' + driverName
        if int(driverStart) != int(start):
            # update driverID in DB isAvailable to not True, set current customer to = CustomerName, CustomerLoc = Start
            newDriver = Driver(driverName, driverStart)
            driverPath, driverDistance = newDriver.driverRoute(driverStart, int(start))
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
        else:
            path = []
            path.append([graph.locations[int(start)][1], graph.locations[int(start)][2]])
            m = folium.Map(location=path[0], tiles='OpenStreetMap', zoom_start=18, control_scale=True)
            folium.Marker(
                location=path[0],
                icon = folium.Icon(color="green", icon="map-marker"),
                popup=startLocation, tooltip="Your Location"
            ).add_to(m)

            return render_template("rideDetails.html", map=m._repr_html_(), customerDistance=customerDistance,
                                   startLocation=startLocation,
                                   endLocation=endLocation, rideCost=rideCost, driverInfo=driverInfo,
                                   driverStatus='Driver has arrived!')
        return render_template("rideDetails.html", map=m._repr_html_(),customerDistance=customerDistance, startLocation=startLocation,
                                endLocation=endLocation,rideCost=rideCost, driverInfo=driverInfo, driverStatus='Driver is on the way')
    else:
        return render_template("rideisHere.html", customerDistance=customerDistance, startLocation=startLocation,
                                endLocation=endLocation, rideCost=rideCost, driverStatus=driverStart)

    

@auth.route('/confirmsharedride', methods=['GET', 'POST'])
@login_required
def confirmsharedride():
    fromLocationlat = request.args.get('fromLocationlat', None)
    fromLocationlong = request.args.get('fromLocationlong', None)
    toLocationlat = request.args.get('toLocationlat', None)
    toLocationlong = request.args.get('toLocationlong', None)
    fromLocationname = request.args.get('fromLocationname', None)
    toLocationname = request.args.get('toLocationname', None)

    return render_template("confirmsharedride.html", fromLocationlat=fromLocationlat, fromLocationlong=fromLocationlong,
                           toLocationlat=toLocationlat, toLocationlong=toLocationlong,
                           fromLocationname=fromLocationname, toLocationname=toLocationname)


@auth.route('/settings')
@login_required
def settings():
    return render_template("settings.html")
