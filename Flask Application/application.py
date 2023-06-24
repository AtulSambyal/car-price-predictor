from flask import Flask,render_template,request,redirect,url_for,flash,session
import pandas as pd
import pickle
import math
import mysql.connector
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="sumit@0031",
    database="atul"
)
car=pd.read_csv("Cleaned car.csv")

app=Flask(__name__)

model=pickle.load(open("LinearRegressionModel.pkl",'rb'))

@app.route('/about')
def home():
    return render_template("about.html")

@app.route('/home')
def index():
    name=sorted(car['Name'].unique()) 
    location=sorted(car['Location'].unique())
    fuel_type=sorted(car['Fuel_type'].unique())
    owner=sorted(car['Owner'].unique())
    year=sorted(car['Year'].unique(),reverse=True)
    company=sorted(car['Company'].unique())

    return render_template("index.html",car_model=name,location=location,fuel_type=fuel_type,owner=owner,year=year,company=company)
@app.route('/predict',methods=['POST'])
def predict():
    company=request.form.get('company')
    car_model=request.form.get('car_model')
    location=request.form.get('location')
    fuel_type=request.form.get('fuel_type')
    owner=request.form.get('owner')
    year=int(request.form.get('year'))
    kms_driven=int(request.form.get('kms_driven'))

    prediction=model.predict(pd.DataFrame([[car_model,location,kms_driven,fuel_type,owner,year,company]],columns=['Name','Location','Kms_driven','Fuel_type','Owner','Year','Company']))
    if prediction[0] <= 10000:
        prediction[0] = 10000
    return str(math.ceil(prediction[0]))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate the credentials and perform login logic
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        if user:
            if 'username' in session:
                return render_template('index.html')
            else:
                return render_template('login.html', logged_in=False)
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)