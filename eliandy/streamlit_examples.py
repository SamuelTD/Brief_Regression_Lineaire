import streamlit as st


col1, col2 = st.columns(2)

with col1 :
    with st.form("form", clear_on_submit=True):
        st.slider("Age", 18, 100)
        st.radio("Sex", ["Male", "Female"])
        st.text_input("Height")
        st.text_input("Weight")
        st.radio("Do you smoke?", ["Yes", "No"])
        st.radio("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])
        
        if st.form_submit_button("Valider"):
            pass

    st.text_input("Test2")
 
with col2:    
    st.text_input("Test")