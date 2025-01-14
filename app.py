import streamlit as st


with st.sidebar:
        st.subheader("Navigation")
        st.page_link("app.py", label="Page d'Accueil")
        st.page_link("pages/test.py", label="Page Utilisateur")

mon_button = st.button("valider")

if mon_button:
    st.write("Bonjour")