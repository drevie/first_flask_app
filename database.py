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
                reviewDate date,
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
                reviewDate date,
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
                CID int,
                reviewDate date,
                foreign key(ReviewID) references Review(ReviewID),
                foreign key(HotelID) references Hotel(HotelID),
                foreign key(CID) references Review(CID)
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
                price int,
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
        # add customer
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Raghav', 9999, 'raaghavbhardwaj@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Dan', 1111, 'Dan@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Milo', 2012, 'raaghavbhardwaj@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Poornima', 2013, 'Dan@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Kevin', 2014, 'raaghavbhardwaj@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Nick', 2015, 'Dan@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Dan Comm Major', 2016, 'raaghavbhardwaj@gmail.com', '12', 'some street'))
        self.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', ('Zhao', 2016, 'Dan@gmail.com', '12', 'some street'))

        # add hotels
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('1', 909090, '34th street', 'New York', 'USA', '1111'))
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('2', 808080, 'Some LA Street', 'California', 'USA', '2222'))
        self.cursor.execute('''INSERT INTO Hotel(HotelID, Phone_no, Street, City, Country, zip) VALUES(?,?,?,?,?,?)''', ('3', 505050, 'Chembur', 'Mumbai', 'India', '3333'))

        # add rooms
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '1', '$500', '2', '8', 'Spacious Room with view for the Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '2', '$600', '3', '9', 'Spacious Room with view for the Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('1', '3', '$700', '4', '10', 'Spacious Room with view for the Skyline', 'Suite'))

        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '1', '$500', '2', '8', 'Overlooks LA streets', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '2', '$600', '3', '9', 'Overlooks LA streets', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('2', '3', '$700', '4', '10', 'Overlooks LA streets', 'Suite'))

        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '1', 'R500', '2', '8', 'Overlooks Mumbai Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '2', 'R600', '3', '9', 'Overlooks Mumbai Skyline', 'Regular'))
        self.cursor.execute('''INSERT INTO Room(HotelID, Room_no, Price, Capacity, Floor_no, Description, Type) VALUES(?,?,?,?,?,?,?)''', ('3', '3', 'R700', '4', '10', 'Overlooks Mumbai Skyline', 'Suite'))

        # add services and breakfast
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (1, "continental", "continental breakfast", "$50"))
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (2, "continental", "continental breakfast", "$50"))
        self.cursor.execute('''INSERT INTO Breakfast(HotelID, bType, description, bprice) VALUES (?,?,?,?)''', (3, "continental", "continental breakfast", "$50"))

        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (1, "massage", "$20"))
        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (2, "massage", "$20"))
        self.cursor.execute('''INSERT INTO Service(HotelID, sType, sCost) VALUES (?,?,?)''', (3, "massage", "$20"))

        # add reservations
        #self.cursor.execute('''INSERT INTO Reservation(InvoiceNo, ResDate, InDate, OutDate, Room_no, HotelID, CID, Cnumber, sType, bType, price) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (1, "5/11/17", "5/12/17", "5/15/17", 1, 1, 1, 5555, "massage", "continental", 500))
        #self.cursor.execute('''INSERT INTO Reservation(InvoiceNo, ResDate, InDate, OutDate, Room_no, HotelID, CID, Cnumber, sType, bType, price) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (2, "5/11/17", "5/12/17", "5/15/17", 1, 1, 1, 5555, "massage", "continental", 400))
        #self.cursor.execute('''INSERT INTO Reservation(InvoiceNo, ResDate, InDate, OutDate, Room_no, HotelID, CID, Cnumber, sType, bType, price) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (3, "5/11/17", "5/12/17", "5/15/17", 2, 3, 2, 5555, "massage", "continental", 1000))
        #self.cursor.execute('''INSERT INTO Reservation(InvoiceNo, ResDate, InDate, OutDate, Room_no, HotelID, CID, Cnumber, sType, bType, price) VALUES(?,?,?,?,?,?,?,?,?,?,?)''', (4, "5/11/17", "5/12/17", "5/15/17", 3, 3, 5, 5555, "massage", "continental", 2000))
        
        """# add room reviews
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (1, 111, 11, 2224, 5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (2, 112, 12, 2224, 2.5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (3, 112, 13, 2224, 4, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (4, 113, 14, 2224, 4.5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (5, 111, 14, 2224, 2, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (6, 111, 15, 2221, 1, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (7, 114, 15, 2222, 4, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (8, 114, 15, 2223, 3, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (9, 115, 16, 2212, 1, "2017-05-05"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (10, 116, 16, 2221, 2, "2017-05-05"))

        # add service reviews
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (10, "massage", 11, 2012, 2.5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (11, "massage", 12, 2222, 5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (12, "lessons", 13, 2223, 4, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (13, "lessons", 14, 2224, 3, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (14, "cleaning", 13, 2225, 1, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (15, "laundry", 11, 2225, 2, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (16, "dry cleaning", 12, 2225, 4, "2017-05-05"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (17, "dry cleaning", 13, 2225, 3, "2017-05-05"))

        # Add Breakfast reviews
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (17, "continental", 13, 2225, 3, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (18, "pancake", 11, 22222, 4, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (19, "pancake", 12, 2225, 1, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (20, "omlette", 13, 2225, 1, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (21, "fruit", 14, 2252, 3, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (22, "continental", 15, 2225, 5, "2017-05-05"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (23, "continental", 11, 2225, 5, "2017-05-05"))
        """
        """
        # add room reviews
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (1, 111, 11, 2012, 5, "5/5/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (2, 112, 12, 2012, 2.5, "1/3/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (3, 112, 13, 2012, 4, "5/3/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (4, 113, 14, 2012, 4.5, "9/14/16"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (5, 111, 14, 2012, 2, "8/11/16"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (6, 111, 15, 2012, 1, "7/12/16"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (7, 114, 15, 2012, 4, "3/16/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (8, 114, 15, 2012, 3, "3/8/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (9, 115, 16, 2012, 1, "3/9/17"))
        self.cursor.execute('''INSERT INTO RoomReview(ReviewId, Room_no, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (10, 116, 16, 2012, 2, "3/12/17"))

        # add service reviews
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (10, "massage", 11, 2012, 2.5, "4/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (11, "massage", 12, 2013, 5, "5/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (12, "lessons", 13, 2014, 4, "2/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (13, "lessons", 14, 2013, 3, "1/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (14, "cleaning", 13, 2015, 1, "3/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (15, "laundry", 11, 2011, 2, "4/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (16, "dry cleaning", 12, 2012, 4, "1/12/17"))
        self.cursor.execute('''INSERT INTO ServiceReview(ReviewId, sType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (17, "dry cleaning", 13, 2015, 3, "2/12/17"))

        # Add Breakfast reviews
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (17, "continental", 13, 2015, 3, "1/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (18, "pancake", 11, 2015, 4, "4/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (19, "pancake", 12, 2015, 1, "3/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (20, "omlette", 13, 2015, 1, "5/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (21, "fruit", 14, 2015, 3, "1/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (22, "continental", 15, 2015, 5, "3/12/17"))
        self.cursor.execute('''INSERT INTO BreakfastReview(ReviewId, bType, HotelID, CID, stars, reviewDate) VALUES(?,?,?,?,?,?)''', (23, "continental", 11, 2015, 5, "1/12/17"))
        """



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