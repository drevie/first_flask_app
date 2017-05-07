import sqlite3

global DB


class Hotel_DB:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = self.db.cursor()

    def spinDB(self):

        self.cursor.execute('''
            CREATE TABLE customers(
            cid INTEGER PRIMARY KEY,
            firstName VARCHAR,
            lastName VARCHAR,
            phone VARCHAR,
            email VARCHAR,
            password VARCHAR)
            ''')

        self.cursor.execute('''
            CREATE TABLE rooms(
            roomID INTEGER PRIMARY KEY,
            bookedFrom DATE,
            bookedTo DATE,
            discount INT
            ) ''')

        self.cursor.execute('''
            CREATE TABLE reservations(
            reservationID INTEGER PRIMARY KEY,
            customerID INTEGER,
            roomID VARCHAR,
            breakfastsOrdered VARCHAR,
            servicesOrdered VARCHAR,
            paymentOwed INT,
            FOREIGN KEY(customerID) REFERENCES customer(cid),
            FOREIGN KEY(roomID) REFERENCES rooms(roomID)
            )''')

        self.cursor.execute('''
            CREATE TABLE reviews(
            reviewID INTEGER PRIMARY KEY,
            reviewCategory VARCHAR,
            customerID INT,
            FOREIGN KEY(customerID) REFERENCES customers(cid)
            )''')


        self.db.commit()

    def insertTestValues(self):
        customers = [
            {
                'firstName': "Daniel",
                'lastName': "Revie",
                'phone': "2016753642",
                'email': "daniel.revie1@gmail.com",
                'password': "Mr J"

            },
            {
                'firstName': "Daniel",
                'lastName': "Revie",
                'phone': "2016753642",
                'email': "daniel.revie1@gmail.com",
                'password': "Mr J"

            },
            {
                'firstName': "Daniel",
                'lastName': "Revie",
                'phone': "2016753642",
                'email': "daniel.revie1@gmail.com",
                'password': "Mr J"

            },
            {
                'firstName': "Daniel",
                'lastName': "Revie",
                'phone': "2016753642",
                'email': "daniel.revie1@gmail.com",
                'password': "Mr J"

            },

        ]

        self.cursor.execute(''' INSERT INTO customers(firstName, lastName, phone, email, password) VALUES (?,?,?,?,?) ''', (customers[0]['firstName'], customers[0]['lastName'], customers[0]['phone'], customers[0]['email'], customers[0]['password']))
        self.cursor.execute(''' INSERT INTO customers(firstName, lastName, phone, email, password) VALUES (?,?,?,?,?) ''', (customers[1]['firstName'], customers[1]['lastName'], customers[1]['phone'], customers[1]['email'], customers[1]['password']))
        self.cursor.execute(''' INSERT INTO customers(firstName, lastName, phone, email, password) VALUES (?,?,?,?,?) ''', (customers[2]['firstName'], customers[2]['lastName'], customers[2]['phone'], customers[2]['email'], customers[2]['password']))
        self.cursor.execute(''' INSERT INTO customers(firstName, lastName, phone, email, password) VALUES (?,?,?,?,?) ''', (customers[3]['firstName'], customers[3]['lastName'], customers[3]['phone'], customers[3]['email'], customers[3]['password']))

    def testPrint(self):
        print("test print")


def init():
    global hotel_db
    # Here we create a temporary db in RAM
    db = sqlite3.connect(':memory:', check_same_thread=False)

    # Create a curson for the db
    cursor = db.cursor()
    hotel_db = Hotel_DB(db, cursor)
    hotel_db.spinDB()
    hotel_db.insertTestValues()