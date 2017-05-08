import sqlite3

global DB


class Hotel_DB:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = self.db.cursor()

    def spinDB(self):

        self.cursor.execute('''
            CREATE TABLE Hotel(
                HotelID int primary key,
                Phone_no varchar(255),
                Street varchar(50),
                City varchar(50),
                Country varchar(50),
                zip int
                )''')

        self.cursor.execute('''
            CREATE TABLE Breakfast(
                HotelID int,
                bType varchar(50),
                description varchar(100),
                bprice real,
                primary key(HotelID, bType),
                foreign key(HotelID) references Hotel(HotelID)
                )''')

        self.cursor.execute('''
            CREATE TABLE Service(
                HotelID int,
                sType varchar(50),
                sCost int,
                primary key(HotelID, sType),
                foreign key(HotelID) references Hotel(HotelID)
            )''')

        self.cursor.execute('''
            CREATE TABLE Room(
                HotelID int,
                Room_no int,
                Price real,
                Capacity int,
                Floor_no int,
                Description varchar(100),
                Type varchar(50),
                primary key(HotelID, Room_no),
                foreign key(HotelID) references Hotel(HotelID)
            )''')

        self.cursor.execute('''
            CREATE TABLE OfferRoom(
                HotelID int,
                Room_no int,
                Sdate date,
                Discount real,
                Edate date,
                primary key(Room_no, HotelID),
                foreign key(HotelID) references Hotel(HotelID)
            )''')

        self.cursor.execute('''
            CREATE TABLE Customer(
                CID integer primary key AUTOINCREMENT,
                email varchar(50),
                address varchar(50),
                Phone_no varchar(50),
                Name varchar(50),
                Password varchar(50)
            )''')

        self.cursor.execute('''
            CREATE TABLE CreditCard(
                Cnumber int,
                BillingAddress varchar(100),
                Name varchar(50),
                SecCode int,
                Type varchar(50),
                ExpDate varchar(50),
                CID int,
                primary key(Cnumber),
                foreign key(Name, CID) references Customer(Name, CID)
            )''')

        self.cursor.execute('''
            CREATE TABLE Review(
                ReviewID integer primary key AUTOINCREMENT,
                Rating int check(Rating>=1 AND Rating<=5),
                TextComment varchar(255),
                CID int,
                foreign key(CID) references Customer(CID)
            )''')

        self.cursor.execute('''
            CREATE TABLE RoomReview(
                ReviewID int,
                Room_no int,
                HotelID int,
                CID int,
                primary key(ReviewID, Room_no, HotelID, CID),
                foreign key(ReviewID) references Review(ReviewID),
                foreign key(Room_no) references Room(Room_no),
                foreign Key(HotelID) references Hotel(HotelID),
                foreign key(CID) references Customer(CID)
            )''')

        self.cursor.execute('''
            CREATE TABLE BreakfastReview(
                ReviewID int,
                bType varchar(50),
                HotelId int,
                CID int,
                primary key(ReviewID, bType, HotelID, CID),
                foreign key(ReviewID) references Review(ReviewID),
                foreign key(HotelID) references Hotel(HotelID),
                foreign key(bType) references Breakfast(bType),
                foreign key(CID) references Review(CID)
            )''')

        self.cursor.execute('''
            CREATE TABLE ServiceReview(
                ReviewID int,
                sType varchar(40),
                HotelID int,
                foreign key(ReviewID) references Review(ReviewID),
                foreign key(HotelID) references Hotel(HotelID),
                primary key(ReviewId, sType, HotelID)
            )''')

        self.cursor.execute('''
            CREATE TABLE Reservation(
                InvoiceNo int,
                ResDate date,
                InDate date,
                OutDate, date,
                Room_no int,
                HotelID int,
                CID int,
                Cnumber int,
                sType varchar(50),
                bType varchar(50),
                primary key(InvoiceNo, HotelID, CID),
                foreign key(Room_no) references Room(Room_no),
                foreign key(HotelID) references Hotel(HotelID),
                foreign key(Cnumber) references CreditCard(Cnumber)
                foreign key(bType) references Breakfast(bType),
                foreign key(sType) references Service(sType)
                foreign key(CID) references Customer(CID)
            )''')

        self.db.commit()

    def commitDB(self):
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
        # add customer
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Raghav', 9999, 'raaghavbhardwaj@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Dan', 1111, 'Dan@gmail.com', '12', 'some street'))

        #add hotels
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('1', 909090, '34th street', 'New York', 'USA', '1111'))
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('2', 808080, 'Some LA Street', 'California', 'USA', '2222'))
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('3', 505050, 'Chembur', 'Mumbai', 'India' ,'3333'))

        #add rooms
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '1', '$500', '2', '8','Spacious Room with view for the Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '2', '$600', '3', '9','Spacious Room with view for the Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '3', '$700', '4', '10','Spacious Room with view for the Skyline', 'Suite'))

        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '1', '$500', '2', '8','Overlooks LA streets', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '2', '$600', '3', '9','Overlooks LA streets', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '3', '$700', '4', '10','Overlooks LA streets', 'Suite'))

        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '1', 'Rs500', '2', '8','Overlooks Mumbai Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '2', 'Rs600', '3', '9','Overlooks Mumbai Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '3', 'Rs700', '4', '10','Overlooks Mumbai Skyline', 'Suite'))

        # add services and breakfast
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (1,"continental", "continental breakfast", "$50"))
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (2,"continental", "continental breakfast", "$50"))
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (3,"continental", "continental breakfast", "$50"))


        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (1,"massage", "$20"))
        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (2,"massage", "$20"))
        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (3,"massage", "$20"))

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