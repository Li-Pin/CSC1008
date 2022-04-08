from customer import Customer
import driver

baseFare = 4.05  # taken from comfortdelgo website
perKMPrice = 0.7  # taken from comfortdelgo website


# customer log in from website
newCustomer = Customer('bob', 123)

# after customer submit ride details
customerPath, customerDistance = newCustomer.getCustomerRide()  # to plot out path
print('your is distance is: ', customerDistance)
print('price will be :', baseFare + customerDistance * perKMPrice)
print('Your Route is :', customerPath)

# after customer book ride
# maxDriverDistance = input('Enter max driver distance: ')

