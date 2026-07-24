import streamlit as st
from utils.auth import login_user

st.set_page_config(page_title="Login")

st.title("🔐 Login")

email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Login"):

    try:
        response = login_user(email, password)

        if response.user:
            st.session_state["user"] = response.user
            st.success("Login successful! 🎉")

            st.switch_page("pages/3_Home.py")

        else:
            st.error("Invalid email or password.")

    except Exception as e:
        st.error(str(e))