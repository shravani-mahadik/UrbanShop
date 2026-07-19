import streamlit as st

st.set_page_config(
    page_title="UrbanShop",
    page_icon="🛍️",
    layout="wide"
)

st.title("🛍️ UrbanShop")

st.write("Welcome to UrbanShop")

st.page_link(
    "pages/3_Signup.py",
    label="Create Account"
)

st.page_link(
    "pages/2_Login.py",
    label="Login"
)