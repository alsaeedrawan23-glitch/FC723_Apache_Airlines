

#Class that stores Apaches seating grid, allows user to check, book and free seats
class SeatingSystem:
   
    # constructor method, its encapsulated so cannot be changed outside of the class
    def __init__(self):
        
        #creatign private dictionary to store all the seat data
        self.__grid = {}

        # The row letters for the Burak757
        self.__rows = ["A", "B", "C", "X", "D", "E", "F"]

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

    #displays the seating layout to the user 
    def show_grid(self):
        
        #
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

           # loop through each column number to the header 
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

        # Check the status and return a message to the user 
        #seat is free
        if status == "F":
            return "Seat " + seat + " is FREE and available to book."
        #seat is reserved
        elif status == "R":
            return "Seat " + seat + " is RESERVED and not available."
        #seat is an aisle and cannot be booked
        elif status == "X":
            return "Seat " + seat + " is an AISLE. No booking can be made here."
        #seat is storage space an cannot be booked
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. No booking can be made here."

    # function that allows the user to book a seat 
    def book_seat(self, seat):
        
        # Check if the seat exists in the grid
        if seat not in self.__grid:
            return "Seat " + seat + " does not exist. Please enter a valid seat."

        # Get the current status of the seat from the dictionary
        status = self.__grid[seat]

        if status == "F":
            # checks status, if seat is free it can be booked, otherwise it cannot
            self.__grid[seat] = "R"
            return "Seat " + seat + " has been successfully BOOKED."
        elif status == "R":
            return "Seat " + seat + " is already RESERVED. Please choose a different seat."
        elif status == "X":
            return "Seat " + seat + " is an AISLE. It cannot be booked."
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. It cannot be booked."

    #function that allows the user to free a seat
    def free_seat(self, seat):
       
        # Check if the seat exists in the grid
        if seat not in self.__grid:
            return "Seat " + seat + " does not exist. Please enter a valid seat."

        # Get the current status of the seat from the dictionary
        status = self.__grid[seat]
        
        #if seat is reserved it can be freed
        if status == "R":
            self.__grid[seat] = "F"
            return "Seat " + seat + " has been successfully FREED and is now available."
        #otherwise it cannot be freed
        elif status == "F":
            return "Seat " + seat + " is already FREE. No action needed."
        elif status == "X":
            return "Seat " + seat + " is an AISLE. It cannot be freed."
        elif status == "S":
            return "Seat " + seat + " is a STORAGE area. It cannot be freed."

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