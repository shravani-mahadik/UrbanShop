import streamlit as st
from utils.auth import signup_user

st.set_page_config(page_title="Signup")

st.title("📝 Create Account")

full_name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Create Account"):

    if password != confirm_password:
        st.error("Passwords do not match")

    else:
        try:
            signup_user(full_name, email, password)
            st.success("Account created successfully!")

        except Exception as e:
            st.error(str(e))