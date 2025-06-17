
import streamlit as st
import pickle
import pandas as pd

def format_to_indian_rupees(amount) :
    if amount < 1000:
        return f"₹ {amount}"

    num_str = str(amount)
    last_three = num_str[-3:]
    rest = num_str[:-3]

    # Insert commas every 2 digits in the rest of the number
    if rest:
        rest = ",".join([rest[max(i - 2, 0):i] for i in range(len(rest), 0, -2)][::-1])
        formatted = f"₹ {rest},{last_three}"
    else:
        formatted = f"₹ {last_three}"

    return formatted

def predict_price(company,model,year,kms,fuel):
    price = pipe.predict(pd.DataFrame([[model,company,year,kms,fuel]],columns=['name','company','year','kms_driven','fuel_type']))
    price = int(price[0])
    if price<=0:
        return 'Too old model'
    price= format_to_indian_rupees(price)

    return 'Predicted Price is around : '+ price

car = pd.read_csv('cleaned_car.csv')
company_models = pickle.load(open('company_model.pkl','rb'))
pipe = pickle.load(open('LinearRegressionModel.pkl','rb'))

st.title('Car Price Predictor')
company = st.selectbox('Enter company name',( car['company'].unique() ))
model = st.selectbox('Enter model name',( company_models[company] ))
year = st.number_input("Enter model year", min_value=0, step=1,value=2020, format="%d")
kms = st.number_input("Enter total distance covered", min_value=0, step=1,value=1000, format="%d")
fuel = st.selectbox('Enter fuel type',(['Petrol','Diesel','LPG']))

if st.button('Predict'):
    price = predict_price(company,model,year,kms,fuel)
    st.text(price)
