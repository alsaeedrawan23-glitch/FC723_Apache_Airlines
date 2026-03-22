#importing modules for generate reference 
import random
import string
#importing module to create and manage the database 
import sqlite3

#Class that stores Apaches seating grid, allows user to check, book and free seats
class SeatingSystem:
   
    # constructor method, its encapsulated so cannot be changed outside of the class
    def __init__(self):
        
        #creating private dictionary to store all the seat data
        self.__grid = {}
        # The row letters for the Burak757
        self.__rows = ["A", "B", "C", "X", "D", "E", "F"]
        #added a set to store all used references so no duplicates occur 
        self.__used_references = set()
        #creates a database file 
        self.__conn = sqlite3.connect("bookings.db")
        # creates cursor object to execute the SQL commands
        self.__cursor = self.__conn.cursor()
        
        # creates the booking database table 
        self.__cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                reference TEXT,
                first_name TEXT,
                last_name TEXT,
                passport TEXT,
                seat TEXT
            )
        """)
        # save the changes to the database 
        self.__conn.commit()
        
        # loop through every column from 1 to 80
        for col in range(1, 81):
            # Loop through every row letter for each column
            for row in self.__rows:

                #combining column number and row letter to create the seat number
                seat = str(col) + row
                
                #aisle seats cannot be booked 
                if row == "X":
                    self.__grid[seat] = "X"
                
                #setting storage areas
                elif row in ["D", "E", "F"] and 5 <= col <= 78:
                    self.__grid[seat] = "S"

                else:
                    # all the other seats are free/normal seats
                    self.__grid[seat] = "F"


    #function that generates unique character for booking reference 
    def generate_reference(self):

        # string.ascii_uppercase gives A-Z and string.digits gives us 0-9
        characters = string.ascii_uppercase + string.digits

        # keep generating until a reference that hasnt been used is generated 
        while True:
            reference = ""
            
            # pick 8 random characters from the characters string 
            for i in range(8):
                reference = reference + random.choice(characters)

            # check if generated reference already exists, if not save and return it 
            if reference not in self.__used_references:
                self.__used_references.add(reference)
                return reference


    #displays the seating layout to the user 
    def show_grid(self):
        
        print("\n========== BURAK757 SEAT LAYOUT ==========")
        print("F = Free  R = Reserved  X = Aisle   S = Storage")

        # loop through each column 20 at a time 
        for start_col in range(1, 81, 20):
            end_col = start_col + 19

            col_header = "     "

            # add each column number to the header 
            for col in range(start_col, end_col + 1):
                col_header = col_header + str(col).ljust(3)
            print(col_header)

            # loop through each row letter
            for row in self.__rows:
                # row letter
                line = "  " + row + ": "

                # loop through each of the 20 columns in this section
                for col in range(start_col, end_col + 1):
                    # combine column number and row letter to get the seat code 
                    seat = str(col) + row
                    
                    #add seat status
                    line = line + self.__grid[seat].ljust(3)

                # print the completed line for this row 
                print(line)


    #function that checks if a specific seat is available 
    def check_availability(self, seat):
        
        # Check if the seat exists in the grid
        if seat not in self.__grid:
            return "Seat " + seat + " does not exist. Please enter a valid seat."

        # Get the current status of the seat from the dictionary
        status = self.__grid[seat]

        #seat is free
        if status == "F":
            return "Seat " + seat + " is FREE and available to book."
        #seat is an aisle and cannot be booked
        elif status == "X":
            return "Seat " + seat + " is an AISLE. No booking can be made here."
        #seat is storage space and cannot be booked
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. No booking can be made here."
        #seat gets stored as a reference instead of just R 
        else:
            return "Seat " + seat + " is RESERVED with reference " + status + "."


    # function that allows the user to book a seat 
    def book_seat(self, seat):
        
        # Check if the seat exists in the grid
        if seat not in self.__grid:
            return "Seat " + seat + " does not exist. Please enter a valid seat."

        # Get the current status of the seat from the dictionary
        status = self.__grid[seat]

        if status == "F":
            #ask the customer for their details before booking
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            passport = input("Enter passport number: ") 
            #generate a unique reference and store it 
            reference = self.generate_reference()
            self.__grid[seat] = reference 
            
            # insert the customer details into the database 
            self.__cursor.execute(""" INSERT INTO bookings (reference, first_name, last_name, passport, seat)
                VALUES (?, ?, ?, ?, ?) """, (reference, first_name, last_name, passport, seat))
            
            # save changes to the database 
            self.__conn.commit()
            
            return "Seat " + seat + " has been successfully BOOKED. Your reference is: " + reference
       
        elif status == "X":
            return "Seat " + seat + " is an AISLE. It cannot be booked."
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. It cannot be booked."
        else: 
            return "Seat " + seat + " is already RESERVED. Please choose a different seat."


    #function that allows the user to free a seat
    def free_seat(self, seat):
       
        # Check if the seat exists in the grid
        if seat not in self.__grid:
            return "Seat " + seat + " does not exist. Please enter a valid seat."

        # Get the current status of the seat from the dictionary
        status = self.__grid[seat]
        
        if status == "F":
            return "Seat " + seat + " is already FREE. No action needed."
        elif status == "X":
            return "Seat " + seat + " is an AISLE. It cannot be freed."
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. It cannot be freed."
        else:
            #remove the reference and free the seat 
            self.__used_references.discard(status)
            self.__grid[seat] = "F"
            
            #delete customer details from the database 
            self.__cursor.execute("DELETE FROM bookings WHERE reference = ?", (status,))
            
            # save changes to the database 
            self.__conn.commit()
            return "Seat " + seat + " has been successfully FREED and is now available."


    #this is an extra functionality that counts and displays the total number of free seats
    def count_available(self):
       
        # Start the counter at zero
        count = 0

        # Loop through every seat in the grid
        for seat in self.__grid:
            # If the seat is free add 1 to the counter
            if self.__grid[seat] == "F":
                count = count + 1

        # Display the total number of free seats to the user
        print("\nTotal number of Free seats available: "+ str(count))