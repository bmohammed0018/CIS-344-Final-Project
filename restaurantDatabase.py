import mysql.connector
from mysql.connector import Error

class RestaurantDatabase:
    def __init__(self,
                 host="localhost",
                 port="3306",
                 database="restaurant_reservations",
                 user='root',
                 password='Bash4212@'):

        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password)
            
            if self.connection.is_connected():
                print("Successfully connected to the database")
                return
        except Error as e:
            print("Error while connecting to MySQL", e)

    def addReservation(self, customer_id, reservation_time, number_of_guests, special_requests):
        ''' Method to insert a new reservation into the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()

            # Check if the customer exists, if not, add the customer
            customer_exists_query = "SELECT customerId FROM Customers WHERE customerId = %s"
            self.cursor.execute(customer_exists_query, (customer_id,))
            customer_exists = self.cursor.fetchone()

            if not customer_exists:
                print("Customer does not exist. Adding new customer...")
                self.addCustomer(customer_id, "N/A")  # Assume the customer gets added directly

            # Proceed with adding the reservation
            query = "INSERT INTO Reservations (customerId, reservationTime, numberOfGuests, specialRequests) VALUES (%s, %s, %s, %s)"
            reservation_data = (customer_id, reservation_time, number_of_guests, special_requests)
            self.cursor.execute(query, reservation_data)
            self.connection.commit()
            print("Reservation added successfully")

    def getAllReservations(self):
        ''' Method to get all reservations from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM Reservations"
            self.cursor.execute(query)
            records = self.cursor.fetchall()
            return records

    def cancelReservation(self, reservation_id):
        ''' Method to cancel a reservation by removing it from the reservations table '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "DELETE FROM Reservations WHERE reservationId = %s"
            self.cursor.execute(query, (reservation_id,))
            self.connection.commit()
            print("Reservation canceled successfully")
            return True
        return False  # Return False if the reservation was not canceled successfully
    

    def addCustomer(self, customer_name, phone_number, email):
        ''' Method to add a new customer to the customers table '''
        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                query = "INSERT INTO Customers (customerName, contactInfo) VALUES (%s, %s)"
                self.cursor.execute(query, (customer_name, f"Phone: {phone_number}, Email: {email}"))
                self.connection.commit()
                print("Customer added successfully")
        except mysql.connector.Error as error:
            print("Failed to add customer: {}".format(error))
        finally:
            if self.connection.is_connected():
                self.cursor.close()
                self.connection.close()


    def findReservations(self, customer_id):
        ''' Method to retrieve all reservations for a specific customer '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "SELECT * FROM Reservations WHERE customerId = %s"
            self.cursor.execute(query, (customer_id,))
            reservations = self.cursor.fetchall()
            return reservations

    def addSpecialRequest(self, reservation_id, special_requests):
        ''' Method to update special requests for a reservation '''
        if self.connection.is_connected():
            self.cursor = self.connection.cursor()
            query = "UPDATE Reservations SET specialRequests = %s WHERE reservationId = %s"
            self.cursor.execute(query, (special_requests, reservation_id))
            self.connection.commit()
            print("Special requests updated successfully")

    # Inside the RestaurantDatabase class

    def updateReservation(self, reservation_id, new_customer_id, new_reservation_time, new_number_of_guests, new_special_requests):
        ''' Method to update an existing reservation '''
        try:
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()

                # Check if the reservation exists
                reservation_exists_query = "SELECT * FROM Reservations WHERE reservationId = %s"
                self.cursor.execute(reservation_exists_query, (reservation_id,))
                reservation_exists = self.cursor.fetchone()

                if reservation_exists:
                    # Update the reservation
                    update_query = "UPDATE Reservations SET customerId = %s, reservationTime = %s, numberOfGuests = %s, specialRequests = %s WHERE reservationId = %s"
                    updated_data = (new_customer_id, new_reservation_time, new_number_of_guests, new_special_requests, reservation_id)
                    self.cursor.execute(update_query, updated_data)
                    self.connection.commit()
                    print("Reservation updated successfully")
                    return True
                else:
                    print("Reservation does not exist")
                    return False
        except mysql.connector.Error as error:
            print("Failed to update reservation: {}".format(error))
            return False
