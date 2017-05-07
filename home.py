
from flask import Flask, render_template, session, request, flash
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
    return render_template('index.html' )


@app.route('/customerRegistration')
def showRegisterTool():
    return render_template('customerRegister.html')


@app.route('/showSignIn')
def showSignInTool():
    return render_template('signIn.html')


@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/showBooking')
def bookHotel():
    return render_template('bookHotel.html')



@app.route('/login', methods=['GET', 'POST'])
def check_login():
    session["username"] = request.form.get("username")
    session["password"] = request.form.get("password")
    if( session["username"] == "9999" ):
        session["logged_in"] = True
    return render_template('login.html') 
'''
def create_user():
    print("SUER MADE")
    return render_template('login.html')
'''
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
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.TEMPLATES_AUTO_RELOAD = True
    app.run(debug=True)
    session["logged_in"] = Flase
    is_auth = False
    session.clear() 
