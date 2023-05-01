from flask import Flask,render_template,request
import pandas as pd
import pickle
import math

car=pd.read_csv("Cleaned car.csv")

app=Flask(__name__)

model=pickle.load(open("LinearRegressionModel.pkl",'rb'))

@app.route('/')
def index():
    name=sorted(car['Name'].unique()) 
    label=sorted(car['Label'].unique())
    location=sorted(car['Location'].unique())
    fuel_type=sorted(car['Fuel_type'].unique())
    owner=sorted(car['Owner'].unique())
    year=sorted(car['Year'].unique(),reverse=True)
    company=sorted(car['Company'].unique())

    return render_template("index.html",car_model=name,label=label,location=location,fuel_type=fuel_type,owner=owner,year=year,company=company)
@app.route('/predict',methods=['POST'])
def predict():
    company=request.form.get('company')
    car_model=request.form.get('car_model')
    label=request.form.get('label')
    location=request.form.get('location')
    fuel_type=request.form.get('fuel_type')
    owner=request.form.get('owner')
    year=int(request.form.get('year'))
    kms_driven=int(request.form.get('kms_driven'))

    predicton=model.predict(pd.DataFrame([[car_model,label,location,kms_driven,fuel_type,owner,year,company]],columns=['Name','Label','Location','Kms_driven','Fuel_type','Owner','Year','Company']))

    return str(math.ceil(predicton[0]))

if __name__=="__main__":
    app.run(debug=True)