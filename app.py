from flask import *
app = Flask(__name__) # provide an argument __name__ to get project name auto
app.secret_key = "QWEWbvbnv67678!@##$$ghghghj" # trhis key will secure your session
# Routing
# Home Page
import pymysql
@app.route("/")
def home():
    # Pull records from database
    con = pymysql.connect(host='localhost', user = 'root', password='',
                          database='myshop_db')

    sql = "select * from products"
    # create a cursor to execute above sql
    cursor = con.cursor()
    # now run sql
    cursor.execute(sql)
    # check num rows returned
    if cursor.rowcount == 0:
        pass
    else:
        # get all product rows
        rows = cursor.fetchall()
        # return the rows to html
        return render_template("index.html", rows = rows)




@app.route('/signup', methods = ['POST','GET'])
def signup():
    if request.method =='POST':
        username = request.form['username']
        email = request.form['email']
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            return render_template('signup.html', message = "Passwords do not match")
        elif len(password1) < 8:
            return render_template('signup.html', message="Must not be less than 8 ters")
        else:
            con = pymysql.connect(host='localhost', user='root', password='',
                                  database='myshop_db')

            sql = "insert into users(username, email, password) values (%s, %s, %s)"
            cursor = con.cursor()
            try:
               cursor.execute(sql, (username, email, password1))
               con.commit()
               return render_template('signup.html', message="Thank you for Registering")
            except:
                return render_template('signup.html', message="Something went wrong")
    else:
        return render_template('signup.html', message="Please Fill your details and submit")


# login
# modcom.co.ke/api/code.txt
@app.route('/signin', methods = ['POST','GET'])
def signin():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']
        # process login
        connection = pymysql.connect(host='localhost', user='root', password='',
                                     database='myshop_db')

        # Create a cursor to execute SQL Query
        cursor = connection.cursor()
        cursor.execute('select * from users where email = %s and password =%s',
                       (email, password))
        # above query should either find a match or not
        # check how may rows cursor found
        if cursor.rowcount ==0:
            return render_template('signin.html', message = 'Wrong Credentials!')
        elif cursor.rowcount ==1:
            # this user is now looged in and the email is set to session.
            session['loggedin'] = email
            return redirect('/')  # after login head to home page
        else:
            return render_template('signin.html', error = 'Something went wrong')
    else:
        return render_template('signin.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/kindergarten")
def kindergarten():
    return render_template('kindergarten.html')

@app.route("/students")
def students():
    return render_template('students.html')


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth
@app.route('/mpesa_payment/<id>', methods = ['POST','GET'])
def mpesa_payment(id):
        if request.method == 'POST':
            phone = str(request.form['phone'])
            amount = str(request.form['amount'])
            # GENERATING THE ACCESS TOKEN
            consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
            consumer_secret = "amFbAoUByPV2rM5A"

            api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials" #AUTH URL
            r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

            data = r.json()
            access_token = "Bearer" + ' ' + data['access_token']

            #  GETTING THE PASSWORD
            timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
            passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
            business_short_code = "174379"
            data = business_short_code + passkey + timestamp
            encoded = base64.b64encode(data.encode())
            password = encoded.decode('utf-8')


            # BODY OR PAYLOAD
            payload = {
                "BusinessShortCode": "174379",
                "Password": "{}".format(password),
                "Timestamp": "{}".format(timestamp),
                "TransactionType": "CustomerPayBillOnline",
                "Amount": amount,  # use 1 when testing
                "PartyA": phone,  # change to your number
                "PartyB": "174379",
                "PhoneNumber": phone,
                "CallBackURL": "https://modcom.co.ke/job/confirmation.php",
                "AccountReference": "account",
                "TransactionDesc": "account"
            }

            # POPULAING THE HTTP HEADER
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest" #C2B URL

            response = requests.post(url, json=payload, headers=headers)
            print (response.text)
            return redirect('/') # here you can redirect top a new route
        else:
            sql = "select * from products where product_id = %s"
            connection = pymysql.connect(host='localhost', user='root', password='',
                                         database='myshop_db')
            cursor = connection.cursor()
            cursor.execute(sql, (id))
            row = cursor.fetchone()
            return render_template('payment.html', row  = row)




app.run(debug=True, port = 4000)
# INSERT
# Select
# update
# delete
