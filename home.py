
from flask import Flask, render_template, session, request, flash, redirect
import database as db
import datetime
import time, random
import pandas as pd
# from flask.ext.mysql import MySQL


# mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'milo'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)

global logged_in
logged_in = False
@app.route('/')
def main():
    return render_template('index.html')


@app.route('/home')
def showHomeTool():
    return render_template('index.html')


@app.route('/customerRegistration')
def showRegisterTool():
    return render_template('customerRegister.html')


@app.route('/registerCustomer', methods=['POST'])
def registerCustomer():

    # first_name = request.args.get('Name1')
    name = request.form['Name']
    phone_number = request.form['Phone Number']
    email = request.form['Email']
    password = request.form['Password']
    passwordConfirm = request.form['Confirm Password']

    print(name)
    print(phone_number)
    print(email)
    print(password)
    print(passwordConfirm)

    db.hotel_db.cursor.execute('''INSERT INTO customers(firstName, lastName, phone, email, password) VALUES(?,?,?,?,?)''', (first_name, last_name, phone_number, email, password))

    return render_template('index.html')


@app.route('/updateCustomer', methods=['PUT'])
def updateCustomer():

    '''
    first_name = request.form['Name1']
    last_name = request.form['Name2']
    phone_number = request.form['Number']
    email = request.form['mail']
    password = request.form['Password']
    passwordConfirm = request.form['Password2']
    '''

    # this is the command to update the databse
    # db.hotel_db.cursor.execute(''' UPDATE customers SET ownerId=? WHERE id=?''', (ownerID, meetingID))


@app.route('/showSignIn')
def showSignInTool():
    return render_template('signIn.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showBooking')
def bookHotel():
    return render_template('bookHotel.html')


@app.route('/login')
def login():
    print("got here")
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def check_login():
    global logged_in
    if request.form['submit'] == 'login':
        # USER LOGIN STUFF HERE
        logged_in = False
        session["logged_in"] = False
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        db.hotel_db.cursor.execute('Select * from Customer where email = ? AND password = ?', (session["username"], session["password"]))
        #print(db.hotel_db.cursor.fetchall())
        data = db.hotel_db.cursor.fetchone()
        if(data):
            logged_in = True
            session["logged_in"] = True
            session["name"] = data[4]
            session["CID"] = data[0]
            return render_template('login.html') 
        else:
            logged_in = False
            session.clear()
            flash("Your login credentials were incorrect")
            return redirect("/login#popup1")
    else:
        # NEW USER STUFF HERE
        name = request.form.get("name")
        phone_no = request.form.get("number")
        email = request.form.get("mail")
        password = request.form.get("password")
        address = request.form.get("address")
        db.hotel_db.cursor.execute('''INSERT INTO customer(name, phone_no, email, password, address) VALUES(?,?,?,?,?)''', (name, phone_no, email, password, address))
        data = db.hotel_db.cursor.execute('''Select * from Customer''')
        print(db.hotel_db.cursor.fetchall())
        flash("User Created sucessfully! Please Log In Now")
        return redirect("/login#popup1")

@app.route('/review', methods=['GET', 'POST'])
def review():
    global rooms, hotel_id
    if request.method == 'POST':
        review_desc = request.form.get("review")
        room_no = request.form.get("room_no")
        hotel_id = request.form.get("hotel_id")
        rating = request.form.get("rating")
        db.hotel_db.cursor.execute('''INSERT INTO Review(Rating, TextComment, CID) VALUES (?, ?, ?)''', (rating, review_desc, session["CID"]))
        db.hotel_db.cursor.execute('''Select ReviewID from Review where Rating = ? AND TextComment = ? AND CID = ?''', (rating, review_desc, session["CID"]))
        reviewID = db.hotel_db.cursor.fetchone()
        db.hotel_db.cursor.execute('''INSERT INTO RoomReview(ReviewID, Room_no, HotelID, CID) VALUES (?, ?, ?, ?)''', (reviewID, room_no, hotel_id, session["CID"]))
        flash("Thank you for reviewing the room!")
        return redirect("/review#popup1")
    return render_template('reviews.html', booked_rooms = rooms, hotels = hotel_id[0])



@app.route('/signout')
def signout():
    global logged_in
    logged_in = False
    session.clear()
    return render_template('index.html')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    global logged_in, check_in, check_out, total_cost, rooms, hotel_id
    if request.method == 'POST':
        # make a reservation here
        name = request.form.get("name")
        cnumber = request.form.get("cnumber")
        cvv = request.form.get("cvv")
        address = request.form.get("address")
        date = request.form.get("date")
        curr_date = datetime.datetime.now()
        curr_date = time.strftime('%Y-%m-%d')
        db.hotel_db.cursor.execute('''
            INSERT into CreditCard(BillingAddress,Name,SecCode,Type,ExpDate,CID) VALUES(?,?,?,?,?,?)''', 
            (address, name, cvv, 'visa', date,session["CID"]))
        for room in rooms:
            print(room)
            db.hotel_db.cursor.execute(''' INSERT into Reservation(InvoiceNo, ResDate, InDate, OutDate, Room_no, HotelID, CID, Cnumber, sType, bType) VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                (random.randint(0,99999), curr_date, check_in, check_out, int(room), hotel_id, session["CID"], cnumber, "massage", "continental" ))
        #db.hotel_db.cursor.execute('''Select * from Reservation''')
        df = pd.read_sql_query("select * from Reservation;", db.hotel_db.db)
        print(df)
    return render_template('payment.html')

global check_in, check_out, total_cost, rooms, hotel_id
check_in = check_out = ""
total_cost = 0
@app.route('/reservation', methods=['GET', 'POST'])
def reservation():
    global logged_in, check_in, check_out, total_cost, rooms, hotel_id

    if request.method == 'POST':
        if request.form['submit'] == 'Search Rooms':
            print("GOT HEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRREEEEEEEEEEEEEEEEEEEEEE")
            country = request.form.get("country")
            state = request.form.get("state")
            check_in = request.form.get("in")
            check_out = request.form.get("out")
            room = request.form.get("room")
            print(check_in)
            print(check_out)
            '''
            db.hotel_db.cursor.execute(''''''Select * from Room where Room_no not in 
                                        (Select res.Room_no from Reservation res where (InDate >= ? and InDate < ?) or 
                                        (OutDate >= ? and OutDate < ?)) AND HotelID in (Select HotelID from Hotel where country = ? AND city = ?) AND Type = ?'''''', 
                                        (check_in, check_out, check_in, check_out, country, state, room))
            '''
            db.hotel_db.cursor.execute('''Select * from Room where Room_no not in 
                                        (Select res.Room_no from Reservation res where
                                        (OutDate > ?)) AND HotelID in (Select HotelID from Hotel where country = ? AND city = ?) AND Type = ?''', 
                                        (check_in, country, state, room))
            return render_template('reservation.html', items = db.hotel_db.cursor.fetchall())
        else:
            if logged_in:
                # We're in booking rooms area
                rooms = request.form.getlist("rooms")
                hotelIDs = request.form.getlist("hotelid")
                cost = request.form.getlist("cost")
                hotel_id = hotelIDs[0]
                total_cost = 0
                for room in rooms:
                    total_cost = total_cost + int(cost[int(room)-1][1:])
                return render_template('payment.html', cost = total_cost)
            else:
                flash("Please Log in to book rooms")
                return redirect("/login#popup1")
    return render_template('reservation.html')
    


@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    if request.method == 'GET':
        # Get User credentials from SQL here and Populate these variables!
        db.hotel_db.cursor.execute('Select * from Customer where email = ? AND password = ?', (session["username"], session["password"]))
        data = db.hotel_db.cursor.fetchone()
        email = " "
        password = " "
        name = " "
        address = " "
        phone = " "
        if data:
            email = data[1]
            password = data[5]
            name = data[4]
            address = data[2]
            phone = data[3]
        print("in update user page thing")
        return render_template('userpage.html', **locals())
    else:
        print("GOT HERE")
        # Update user credentials here
        name = request.form.get("name")
        phone_no = request.form.get("number")
        email = request.form.get("mail")
        password = request.form.get("password")
        address = request.form.get("address")
        db.hotel_db.cursor.execute('''UPDATE Customer set name = ?, password = ?, email = ?, phone_no = ?, address = ? WHERE CID = ?''', (name, password, email, phone_no, address, session["CID"]))
        db.hotel_db.cursor.execute('Select * from Customer')
        print(db.hotel_db.cursor.fetchall())
        #db.hotel_db.db.commit()
        flash("Details updated successfully!")
        print("done processing all data")
        return redirect("/user_page#popup1")


@app.route('/header')
def header():
    return render_template('login.html')


@app.route('/adminShell')
def printStates():

    continueFlag = True
    while(continueFlag):
        print("You are in the admin shell")


        print("Enter 1 to comute highest rated room type for each hotel")
        print("Enter 2 to compute 5 best customers")
        print("Enter 3 to compute highest rated breakfast across all hotels")
        print("Enter 4 to compute highest rated service acrross all hotels")
        print("Enter 0 to exit shell")

        selection = int(input())

        if(selection == 0):
            continueFlag = False

        elif(selection == 1 or selection == 2 or selection == 3 or selection == 4):

            print("please enter dates to search from in format YYYY-MM-DD")
            dateStart = input()

            print("please enter date to search to in format YYYY-MM-DD")
            dateEnd = input()

            if(selection == 1):

                db.hotel_db.cursor.execute('''SELECT HotelID, Room_no, stars FROM RoomReview 
                                              WHERE (stars = (SELECT max(stars) FROM RoomReview)) AND (reviewDate BETWEEN date(?) AND date(?))
                                              GROUP BY HotelID ''', (dateStart, dateEnd))

                maxReviews = db.hotel_db.cursor.fetchall()

                for i in range(len(maxReviews)):
                    print("Max reviews: " + str(maxReviews[i]))


            elif(selection == 2):

                db.hotel_db.cursor.execute('''SELECT * FROM Customer 
                                              WHERE (stars = (SELECT max(stars) FROM RoomReview)) AND (reviewDate BETWEEN date(?) AND date(?))
                                              GROUP BY HotelID ''', (dateStart, dateEnd))

                maxReviews = db.hotel_db.cursor.fetchall()

                for i in range(len(maxReviews)):
                    print("Max reviews: " + str(maxReviews[i]))

            elif(selection == 3):

                db.hotel_db.cursor.execute('''SELECT * FROM BreakfastReview 
                                              WHERE (stars = (SELECT max(stars) FROM BreakfastReview)) AND (reviewDate BETWEEN date(?) AND date(?))
                                              GROUP BY HotelID ''', (dateStart, dateEnd))

                maxReviews = db.hotel_db.cursor.fetchall()

                for i in range(len(maxReviews)):
                    print("Max reviews: " + str(maxReviews[i]))

            elif(selection == 4):

                db.hotel_db.cursor.execute('''SELECT * FROM ServiceReview 
                                              WHERE (stars = (SELECT max(stars) FROM ServiceReview)) AND (reviewDate BETWEEN date(?) AND date(?))
                                              GROUP BY HotelID ''', (dateStart, dateEnd))

                maxReviews = db.hotel_db.cursor.fetchall()

                for i in range(len(maxReviews)):
                    print("Max reviews: " + str(maxReviews[i]))

            print("press enter to continue")
            input()

        else:
            print("incorrect input")
            print(selection)



    pass


'''
@app.route('/signUp',methods=['POST', 'GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()

'''

if __name__ == "__main__":
    global db

    db.init()

    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)
    session["logged_in"] = False
    is_auth = False
    session.clear()
