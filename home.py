
from flask import Flask, render_template, session, request, flash, redirect
import database as db
# from flask.ext.mysql import MySQL


# mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'milo'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


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
    first_name = request.form['Name1']
    last_name = request.form['Name2']
    phone_number = request.form['Number']
    email = request.form['mail']
    password = request.form['Password']
    passwordConfirm = request.form['Password2']

    print(first_name)
    print(last_name)
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
    if request.form['submit'] == 'login':
        # USER LOGIN STUFF HERE
        session["logged_in"] = False
        session["username"] = request.form.get("username")
        session["password"] = request.form.get("password")
        if(session["username"] == "9999"):
            session["logged_in"] = True
            return render_template('login.html') 
        else:
            flash("Your login credentials were incorrect")
            return redirect("/login#popup1")
    else:
        # NEW USER STUFF HERE
        return render_template('login.html')


@app.route('/signout')
def signout():
    session.clear()
    return render_template('index.html')


@app.route('/reservation')
def reservation():
    return render_template('reservation.html')


@app.route('/user_page', methods=['GET', 'POST'])
def user_page():
    if request.method == 'GET':
        # Get User credentials from SQL here and Populate these variables!
        username = "user"
        password = "me"
        fname = "cream cheese"
        lname = "ketchup"
        email = "me@me"
        phone = "112233"
        print("in update user page thing")
        return render_template('userpage.html', **locals())
    else:
        # Update user credentials here
        username = request.form['submit']
        password = request.form['password']
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['mail']
        phone = request.form['number']


@app.route('/header')
def header():
    return render_template('login.html')


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
