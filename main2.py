from customer import Customer
from matching import NewBooking
import graphADT
from driver import Driver

baseFare = 4.05  # taken from comfortdelgo website
perKMPrice = 0.7  # taken from comfortdelgo website


# customer log in from website
newCustomer = Customer('bob') # get from DB

# after customer submit ride details
start = input('Enter Start Point: ')  # to replace with form.get.(=start)
end = input('Enter End Point: ')  # to replace with form.get.(=end)
maxDist = input('Enter a max distance for driver: ')
customerPath, customerDistance = newCustomer.getCustomerRide(start, end)  # get from DB
print('your is distance is: ', customerDistance)
print('price will be :', baseFare + customerDistance * perKMPrice)
print('Your Route is :', customerPath)
print('Your starting location is :', customerPath[0])

# after customer book ride

booking = NewBooking(int(start), int(maxDist), newCustomer.name)
driverStart, driverID, driverName = booking.finddriver()

if driverStart != 'No driver':
    print('Driver is at', int(driverStart))
    # update driverID in DB isAvailable to not True, set current customer to = CustomerName, CustomerLoc = Start
    print('your driver is :', driverName)
    # End of Customer stuff
    # newDriver = Driver(driverName, driverStart)
    # driverPath, driverDistance = newDriver.driverRoute(start)
    # print('your driver is ', driverDistance, 'KM away')
    # print('your drivers route is', driverPath)
else:
    print('No driver is available!')

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


