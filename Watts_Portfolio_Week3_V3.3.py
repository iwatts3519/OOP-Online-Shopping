# ******************** Intro ********************
#
# For the purposes of this not every method has been created, and it possibly goes beyond the scope of what was required
# However, it has been an excellent learning tool as I have not programmed using OOP before so I wanted to
# learn as much as possible
#
# Certain assumptions have been made - currently as soon as the programme finishes running all of the data is lost In
# a real implementation I would have incorporated a simple database to hold all of the data for the online ordering
# system. I have not implemented user login, though again, I recognise that this would be necessary. I also have only
# minimally coded the Transaction Class, simply returning a string that says payment has been made. I also
# have not implemented reviews for items as this would involve a user logging in after purchase and saving state,
# which I haven't modelled in the diagram and I believe it goes beyond the complexity of what is asked for here.
#
# Within this program I have implemented __repr__ dunder methods for every class. I appreciate that __repr__ is to
# create a representation of the object for the program, and __str__ should be used to create a readable form but for
# brevity I have chosen to simply implement __repr__ in a way that will work for both, as in the absence of a __str__
# method, Python will use __repr__

# ******************** Complexity ********************
# All of the methods implemented in this solution have a Time Complexity of O(1), apart from list_categories(),
# list_items(), list_all_items() and add_items() which have a Time Complexity of O(n) because they loop through
# the items or categories, potentially n times. Because these methods also do assignment as part of their
# implementation they also have a Space Complexity of O(N). If we were using a database and writing to that
# rather than creating lists the Space Complexity could be reduced.

# Used to add today's date to the basket
from datetime import date


# ******************** Person Class ********************
# The Person class is a base class from which staff and customer are derived. It initialises all of the variables
# common to both and defines methods that are also common to both. For the purposes of this exercise address is just
# a string with no validation, as is telephone number, and password does not actually do anything - i.e. there is no
# log in procedure - rather it is simulated later on
class Person:

    def __init__(self, user_name, user_password, name, email, address=None, tel_number=None):
        self.user_name = user_name
        self.user_password = user_password
        self.name = name
        self.email = email
        self.address = address
        self.tel_number = tel_number

    def change_password(self, new_password):
        self.user_password = new_password

    def set_address(self, address):
        self.address = address

    def get_address(self):
        return self.address

    def set_tel_number(self, tel_number):
        self.tel_number = tel_number

    def get_tel_number(self):
        return self.tel_number


# ******************** Staff Class ********************
# Extends the User class by adding in parameters for staff number and department
# A new method has been added allowing the staff member to create items
# A new method has been added to allow a staff member to create categories
class Staff(Person):
    # A class variable is used so that we can create a list of all the members of staff and dynamically create staff
    # numbers
    staff_list = []

    def __init__(self, user_name, user_password, name, email, department, address=None, tel_number=None):
        Person.__init__(self, user_name, user_password, name, email, address=None, tel_number=None)
        # Adds the newly created object to the list of staff that belongs to the Class
        Staff.staff_list.append(self)
        # Sets staff number to be the length of the staff_list after the append has happened (which basically
        # increments the staff ID by 1 every time a new member of staff is created
        self.staff_id = len(Staff.staff_list)
        self.department = department
        self.address = address
        self.tel_number = tel_number

    def __repr__(self):
        return f"********** New Staff Member Created **********\nStaff ID is {self.staff_id}\nName is {self.name}\n" \
               f"Username is {self.user_name}\nDepartment is {self.department}\nPassword is {self.user_password}\n" \
               f"Email Address is {self.email}\nAddress is {self.get_address()}\nTelephone Number is" \
               f"{self.get_tel_number()}\n"

    # The following two are static methods as they may be called even if a member of staff does not exist
    # Items and Categories could be created in the database before a user is created. You could use these to iterate
    # over a list of items or categories read from a CSV file or a database to create the objects
    @staticmethod
    def create_item():
        print("********** Creating a New Item **********\n")
        Item(input("Please enter the name of the item: "),
             input("Please enter a description: "),
             input("Please enter an image: "), float(input("Please enter a price: ")),
             int(input(f"Please enter a category from {Category.list_categories()} ")),
             [], int(input("Please enter the number of items in stock: ")))

    @staticmethod
    def create_category():
        print("********** Creating a New Category **********\n")
        Category(input("Please Type category Name "))


# ******************** Customer Class ********************
# The Customer class extends the user class by assigning a customer number
# to the customer and adding methods for adding and viewing payment methods
# A method has been added called shop() which allows the customer to add items to a basket
class Customer(Person):
    # Same as the staff class, allows us to keep a list of customers
    cust_list = []

    def __init__(self, user_name, user_password, name, email, address=None,
                 tel_number=None):
        Person.__init__(self, user_name, user_password, name, email, address=None, tel_number=None)
        # Uses the same implementation as the Staff Class to dynamically create Customer IDs
        Customer.cust_list.append(self)
        self.customer_id = len(Customer.cust_list)
        self.payment_types = []
        self.payment_type = None
        self.address = address
        self.tel_number = tel_number

    def __repr__(self):
        return (f"********** New Customer Created **********\nCustomer ID is {self.customer_id}\nName is {self.name}\n"
                f"Username is {self.user_name}\n"
                f"Password is {self.user_password}\nEmail Address is {self.email}\n"
                f"Address is {self.get_address()}\nTelephone Number is {self.get_tel_number()}\n")

    # Two methods for adding and retrieving payment methods - these are stored as strings and in a real
    # implementation payment method would be a class in itself. The add_payment method adds the payment
    # type to a list for that customer, and get_payment() displays a list of payment types
    def add_payment(self, payment_type):
        print("********** Payment Type Added **********\n")
        self.payment_types.append(payment_type)

    def get_payment(self):
        print("********** here is a list of payment types **********\n")
        return self.payment_types

    # The customer is able to shop by adding items to a basket (a separate class). Shop continually loops around
    # adding items to the basket while the customer answers the question with an upper or lower case y. Each time round
    # the customer is updated with the total of the basket, and as soon as the customer says they do not
    # want to continue the basket is printed
    def shop(self):
        print("**************************************************\n")
        print("********** Welcome to Ian's Online Shop **********\n")
        print("**************************************************\n")
        basket = Basket(self.customer_id)
        value = True
        while value:
            for item in Item.items:
                print(f"Item Number {item.item_id}: {item.item_name}")
            choice = int(input("What ID Number would you like to add to your basket: "))
            for item in Item.items:
                if item.item_id == choice:
                    basket.add_items(choice)
                    print(f"{item.item_name} has been added to your basket")
                    print(f"Your basket total is {round(basket.total, 2)}")
            shop_more = input("Would you like to shop some more - Y/N: ")
            if shop_more.lower() == "y":
                value = True
            else:
                value = False
        print("********** Basket Details **********\n")
        print(basket)
        payment = input(f"Please choose a payment method from {self.payment_types}: ")
        payment = Transaction(basket.total, payment)
        print(payment.make_payment())


# ******************** Item Class ********************
#     The Item class holds details of all the items sold by the online store.
#     __add__ and __sub__ have been redefined for easily changing stock levels
#     __repr__ has been redefined so that any time the object is returned it returns
#     the value of item_name
class Item:
    # A class variable is created which will hold a list of all items
    items = []

    def __init__(self, name, description, image, cost, category_id, review, stock):
        # The object created is added to the Class variable 'items' list
        Item.items.append(self)
        self.item_id = len(Item.items)
        self.item_name = name
        self.item_description = description
        self.item_image = image
        self.item_cost = cost
        self.item_category_id = category_id
        self.item_review = review
        self.item_stock_level = int(stock)

    def __add__(self, other):
        print("********** Stock Increased **********\n")
        print(f"Stock Level is increasing by {other} to {self.item_stock_level + other}\n")
        self.item_stock_level += other
        return self.item_stock_level

    def __sub__(self, other):
        print("********** Stock Decreased **********\n")
        print(f"Stock Level is decreasing by {other} to {self.item_stock_level - other}\n")
        self.item_stock_level -= other
        return self.item_stock_level

    def __repr__(self):
        return self.item_name

    # The following is a static method that lists all items regardless of category or stock level
    @staticmethod
    def list_all_items():
        lists = []
        for item in Item.items:
            lists.append(f"{item.item_id} - {item}")
        return lists


# ******************** Category Class ********************
# The Category class keep track of the categories of items
# It uses a numerical category_id which is referenced in the
# item list and is used to list all items that match the
# category id. It is created dynamically using the same solution as
# Staff, Customer and Item
class Category:
    categories = []

    def __init__(self, name):
        Category.categories.append(self)
        self.category_id = len(Category.categories)
        self.category_name = name

    def __repr__(self):
        return self.category_name

    def list_items_category(self):
        lists = []
        for item in Item.items:
            if item.item_category_id == self.category_id:
                lists.append(item)
        return lists

    @staticmethod
    def list_categories():
        lists = []
        for category in Category.categories:
            lists.append(f"{category.category_id} - {category}")
        return lists


# ******************** Basket Class ********************
# A basket is created for a particular customer_id. It is created from the shop() method of customer
# It is initialised with an argument for customer_id, and then also initialises variables for
# a list of items, a total amount due and an item_id initially set to None
class Basket:
    def __init__(self, customer_id):
        self.items = []
        self.total = 0
        self.date = date.today()
        self.customer_id = customer_id
        self.item_id = None

    def __repr__(self):
        if not self.items:
            return "Your basket is empty"
        else:
            return f"Your Basket dated {self.date} has {len(self.items)} items in it which are \n" + "\n".join(
                self.items) + f"\nand the total of the basket is {round(self.total, 2)}."

    # add items is a method of the basket and uses the Class variable items from the Item Class to loop through and
    # find the item that is trying to be added. Once found it is added to the list of items, and the total of the
    # basket is updated with the cost of the item
    def add_items(self, item_id):
        self.item_id = item_id
        for item in Item.items:
            if item.item_id == self.item_id:
                self.items.append(item.item_name)
                item - 1
                self.total += item.item_cost


# ******************** Transaction Class ********************
# Once someone has indicated that they have finished shopping the shop() method of the Customer Class asks the user
# to choose a payment method. No verification has been added, though the previously added payment types are
# displayed for reference. Once they choose a payment method, the amount and method are passed to the Transaction
# class, which actually just returns a nicely formatted string telling them that payment has been made. If this was a
# proper implementation then this would link up to a payment API to process the transaction
class Transaction:
    def __init__(self, amount, payment_type):
        self.amount = amount
        self.payment_type = payment_type

    def __repr__(self):
        return f"You have made a payment of {round(self.amount, 2)} using {self.payment_type}\nThank you for " \
               f"shopping with us "

    def make_payment(self):
        return self


# ******************** Testing ********************
# I realise that all of this would actually be tied up with a GUI possibly using tkinter for an in house application
# , though more probably using something like Django to create a web application. However, here I have tried
# to recreate that experience, when a staff member adds items and categories and when the customer shops


# Create Two members of staff and print them out
staff_1 = Staff("iwatts", "password", "Ian Watts", "iwatts@domain.com", "Admin")
staff_2 = Staff("gwatts", "password", "Gabi", "gabi@domain.com", "Stock Control")
print(staff_1)
print(staff_2)

# Create Two customers of staff and print them out
cust_1 = Customer("ewatts", "pssword", "Emily Watts", "Emily@domain.com")
cust_2 = Customer("kwatts", "password", "Katie Watts", "katie@domain.com")
print(cust_1)
print(cust_2)

# Use staff 1 to create categories and items - Category and Item ID are created dynamically
staff_1.create_category()
staff_1.create_category()
staff_1.create_item()
staff_1.create_item()

# list the categories and all items
print(Category.list_categories())
print(Item.list_all_items())

# Create category and item independent of staff
beauty = Category("Beauty")
lipstick = Item("Lipstick", "Beautiful Lipstick", "Path", 4.99, 3, [], 5)

# list the categories and all items
print(Category.list_categories())
print(Item.list_all_items())

# Increase and decrease the stock of lipstick
print("********** Stock Control **********\n")
print(f"Current Stock Levels for {lipstick} are {lipstick.item_stock_level}")
lipstick + 1
lipstick - 2

# Add payment methods for Customer 1
cust_1.add_payment("Mastercard")
cust_1.add_payment("Paypal")
print(cust_1.get_payment())

# Allow Customer 1 to add items into the basket
cust_1.shop()
