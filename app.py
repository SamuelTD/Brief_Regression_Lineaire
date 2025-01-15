import streamlit as st
import pickle
import pandas as pd

if "model" not in st.session_state:
    st.session_state.model = pickle.load(open("model.pickle", "rb"))
    st.session_state.app_state = 0

match st.session_state.app_state:
    #Landing page
    case 0:
        st.title("Welcome to :red[Assur'Aimant]")
        st.header("the world's leader in insurances of all types!")
        st.image("pictures/logo.jpeg", width=500)
        st.header("Navigation :")
        if st.button("I want to estimate my insurance charges."):
            st.session_state.app_state = 1
            st.rerun()
        
        if st.button("I want to see stats."):
            st.session_state.app_state = 2
            st.rerun()
     
    #Client prediction form   
    case 1:
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
                try:
                    height_m = int(height)/100
                    weight_m = int(weight)
                    bmi = weight_m / (height_m)**2
                    if bmi <= 100:
                        columns = ["age", "sex", "children", "bmi", "smoker", "region"]
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
                        prediction = st.session_state.model.predict(data)[0]
                        st.write(f"Your estimated charges are ${round(prediction, 2)}.")
                    else:
                        st.error("There is an issue with your entered values for height and/or weight, please check them.")
                except:
                    st.error("Please enter valid values.")
        
        if st.button("Back"):
            st.session_state.app_state = 0
            st.rerun()
    #Employee page (stats...)
    case 2:
        st.title("Employee dashboard")
        st.scatter_chart([i for i in range(0, 200)])
        if st.button("Back"):
            st.session_state.app_state = 0
            st.rerun()
        
      