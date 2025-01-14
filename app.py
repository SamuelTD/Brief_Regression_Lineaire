import streamlit as st
import pickle
import pandas as pd

if "model" not in st.session_state:
    model = pickle.load(open("model.pickle", "rb"))
    
columns = ["age", "sex", "children", "bmi", "smoker", "region"]

st.title("Subscription Form")
with st.form("form", clear_on_submit=False):
    age = st.slider("Age", 18, 100)
    sex = st.radio("Sex", ["Male", "Female"])
    children = st.number_input("How many children de you have?", 0, 10)
    height = st.text_input("Height (in cm)")
    weight = st.text_input("Weight (in kg)")
    smoking = st.radio("Do you smoke?", ["Yes", "No"])
    region = st.pills("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])
    
    if st.form_submit_button("Validate"):
        
        height_m = int(height)/100
        bmi = int(weight) / (height_m)**2
        data = {}
        for col in columns:
            match col:
                case "age":
                    data[col] = age
                case "sex":
                    data[col] = sex.lower()
                case "children" :
                    data[col] = children
                case "bmi":
                    data[col] = bmi
                case "smoker" :
                    data[col] = smoking.lower()
                case "region":
                    data[col] = region.lower()      
        data = pd.DataFrame(data, index=[0])      
        # st.write(data)     
        bins = [0, 18.5, 24.9, 29.9, 40, 100]  # Tranches de BMI
        labels = ['Sous-poids', 'Poids normal', 'Surpoids', 'Obésité', 'Obésité sévère']
        data['BMI_category'] = pd.cut(data['bmi'], bins=bins, labels=labels, right=False)
        prediction = model.predict(data)[0]
        st.write(f"Your estimated charges are ${round(prediction, 2)}.")
