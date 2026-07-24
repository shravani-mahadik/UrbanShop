import streamlit as st
from utils.auth import signup_user

st.set_page_config(
    page_title="Signup",
    page_icon="📝"
)

st.title("📝 Create Account")
st.write("Create your UrbanShop account")

full_name = st.text_input("Full Name")
email = st.text_input("Email")
password = st.text_input("Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

if st.button("Create Account", use_container_width=True):

    if not full_name or not email or not password or not confirm_password:
        st.warning("Please fill in all fields.")

    elif password != confirm_password:
        st.error("Passwords do not match.")

    else:
        try:
            response = signup_user(full_name, email, password)

            if response.user:
                st.success("🎉 Account created successfully!")
                st.info("You can now log in from the Login page.")
            else:
                st.error("Unable to create account.")

        except Exception as e:
            st.error(f"Error: {e}")