from datetime import datetime

#Camp details - Nested Dictionary
camps = {
  "paradise villas": {
    "Per Day": 370,
    "Card Fee": 4.00,
    "Discount": 10,
    "VAT": 15
  },
  "sunshine hut": {
    "Per Day": 280,
    "Card Fee": 3.50,
    "Discount": 10,
    "VAT": 15
  },
  "standard cabin": {
    "Per Day": 200,
    "Card Fee": 3.00,
    "Discount": 5,
    "VAT": 15
  },
  "treehouse": {
    "Per Day": 160,
    "Card Fee": 2.50,
    "Discount": 5,
    "VAT": 15
  },
  "classic tipi": {
    "Per Day": 120,
    "Card Fee": 2.00,
    "Discount": 5,
    "VAT": 15
  }
}

#Sign in credentials
user = "admin"
passWord = "password"

#Intialize days variable for date input check 
days = None

#Function to check date input is valid
def dateChecker (date):
    if date == datetime.strptime(date, '%d-%m-%Y'):
       return(date)

#Customer reservation to be stored here
bookingDetails = {
  "Customer Name:": "None",
  "Email": "None",
  "Address": "None",
  "Contact Number": 0,
  "Camp": "None",
  "Check In": 0,
  "Check Out": 0,
  "Days": 0,
  "Discount": 0,
  "VAT": 0,
  "Total Cost": 0
}

#Subtotal stored here
subTotal = {
  "Cost per day": 0,
  "Cost before fees": 0,
  "Card Fee": 0,
  "Discount Applied": 0,
  "VAT": 0
}


#Function to write to txt file
def confirmation(details):
  with open("confirmation.txt", "a") as details:
    details.write(str(bookingDetails) + '\n' + '\n')
    details.close()
    return details


#Function to read txt file
def allBookings(file):
  with open(file, "r") as campBookings:
    fileContent = campBookings.read()
    print(fileContent)

#Function to calculate total cost of stays
def bookingCost(campName, days):
#store dictionary info in new variable
  camp = camps[campName]
#Store dictionary key value pairs in new variables
  perDayRate = camp["Per Day"]
  cardFee = camp["Card Fee"]
  discount = camp["Discount"]
  vat = camp["VAT"]
#Calculate total cost per day 
  total = days * perDayRate
#Append values to subtotal/booking confirmation
  subTotal["Cost per day"] = perDayRate
  subTotal["Cost before fees"] = total
#Calculate total cost plus card fee
  subTotal["Card Fee"] = cardFee
  total += cardFee
#Loop for discount if over 14 days - append to booking after calculation
  if days >= 14:
    addDiscount = (discount / 100) * total
    bookingDetails["Discount"] = round(addDiscount)
#Remove discount percentage from total cost 
    total -= addDiscount
#Calculate VAT to the total cost
  tax = (round(vat) / 100) * total
  bookingDetails["VAT"] = round(tax)
  subTotal["VAT"] = round(tax)
  total += tax
  #return total cost 
  return (total)


#Function for entering customer details
def customerDetails():
  print("""
      - Customer Details -
  
                      """)
  customerName = input("\nPlease enter the customers full name:\n")
  address = input("\nPlease enter the customers address:\n")
  email = input("\nPlease enter the customers email:\n")
  mobile = input("\nPlease enter the contact number of the customer:\n")
  bookingDetails["Customer Name:"] = customerName
  bookingDetails["Email"] = email
  bookingDetails["Address"] = address
  bookingDetails["Contact Number"] = mobile
#Once details have been entered call the booking function instead of going to the main menu
  makeABooking()


#Function for making a booking
def makeABooking():
#Loop over camp names and print them
  print("""
     - Accommodation Available -
  
  """)
  for camp in camps:
    print("  \u2022 ", camp)
    print(" ")
  while True:
#Store input values for accomodation booked and days staying
    campName = input("Which camp would you like to book?\n").lower()
    if campName not in camps:
      print("\u203C" "ERROR: Camp does not exist. Please try again")
    else:
      while True:
#User can choose dates in DD-MM-YY format
#Check arrival date is valid
        checkIn = input(
        "   \nWhich date would you like to check-in? (DD-MM-YYYY)\n")
        try:
            dateChecker(checkIn)
            break
        except:
             print("\u203C" "ERROR: Not a valid date. Please try again (DD-MM-YYYY)")
#Check departure date is valid       
      while True:
        checkOut = input(
        "\nWhat date would you like to check-out? (DD-MM-YYYY)\n")
        try:
            dateChecker(checkOut)
            break
        except:
           print("\u203C" "ERROR: Not a valid date. Please try again (DD-MM-YYYY)")        
#Use days to convert the float for timedelta - calculate how many days staying
      arr = (datetime.strptime(checkIn, '%d-%m-%Y'))
      dept = (datetime.strptime(checkOut, '%d-%m-%Y'))
      days =  (dept- arr).days
      break
#Call booking cost function
  total = bookingCost(campName, days)
#Print totalCost of stay with subtotal data
  print(
    "\nYour Subtotal is: \n" + "Cost per day: £" +
    str(subTotal["Cost per day"]) + " for", str(days), "days" + "\n" +
    "Total cost before fees: £" + str(subTotal["Cost before fees"]) + "\n" +
    "Card Fee: £" + str(subTotal["Card Fee"]) + "\n" + "VAT: £" +
    str(subTotal["VAT"]) + "\n" + "This stay also has a discount of £" +
    str(bookingDetails["Discount"]) + " for staying over 14 days" + "\n" +
    "\nThe total cost of your stay will be £", round(total), "\n")
  bookingDetails["Total Cost"] = round(total)
  confirm = input("Would like to confirm the booking: y/n\n").lower()
  if confirm == "y":
#Once the the booking is confirmed all data is append to the booking details dictionary and written to txt file
    bookingDetails["Camp"] = campName
    bookingDetails["Days"] = days
    bookingDetails["Check In"] = checkIn
    bookingDetails["Check Out"] = checkOut
    print("Your booking is confirmed at" + " " + campName + " " + "for " +
          str(days) + " " + "days")
    details = open("confirmation.txt", "a")    
    confirmation(details)
  else:
    print("This booking has not been confirmed")
    return total


#Function for reading all previous bookings in the txt file
def viewABooking():
    print("""
      - All Bookings at Carribean Camping -
""")
#Check for txt file - If not created print except
    try:
         allBookings("confirmation.txt")
    except:
          print("""
        - No previous bookings - 
""")


#Login function - With 3 attempts to login correctly
def logon():
  for loginAttempts in reversed(range(3)):

#Inputs for login
    print("""
       - LOGIN -
""")
    username = input("Please enter your username:\n").lower()
    print("")
    password = input("Please enter your password:\n").lower()
#Compare details for login
    if username == user and password == passWord:
      print("")
      print("You have successfully logged in as", username)

#Stop loop if true
      break


#Login attempts loop
    else:
      print("Please try again - You have ", loginAttempts, "attempts left")
  else:
    print("ACCESS DENIED - Please contact your administrator")

logon()

#Main Menu function
while True:
  print("""

   \U0001F334 WELCOME TO CARRIBBEAN CAMPING \U0001F334

   
            -- MAIN MENU --
   
   1 - Enter customer details
   2 - Making a Booking
   3 - View Bookings
   4 - Logout
  """)
  options = input("Please choose an option: ")
  print("")
  if options == "1":
    customerDetails()
  elif options == "2":
    makeABooking()
  elif options == "3":
    viewABooking()
  elif options == "4":
    print("You have logged out successfully")
    logon()

