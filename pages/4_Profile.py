import streamlit as st
from utils.database import (
    get_profile,
    update_profile
)

# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="My Profile",
    page_icon="👤",
    layout="centered"
)

# =====================================
# LOGIN CHECK
# =====================================

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
    st.stop()

user = st.session_state["user"]

# =====================================
# SIDEBAR
# =====================================

st.sidebar.title("🏪 UrbanShop")
st.sidebar.write(f"👤 {user.email}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/1_Login.py")

# =====================================
# GET PROFILE
# =====================================

profile = get_profile(user.id)

if profile is None:
    st.error("Unable to load profile.")
    st.stop()

# =====================================
# PAGE TITLE
# =====================================

st.title("👤 My Profile")
st.caption("Manage your personal information")

st.divider()

# =====================================
# PROFILE FORM
# =====================================

with st.form("profile_form"):

    full_name = st.text_input(
        "Full Name",
        value=profile.get("full_name", "")
    )

    email = st.text_input(
        "Email",
        value=user.email,
        disabled=True
    )

    phone = st.text_input(
        "Phone Number",
        value=profile.get("phone", "")
    )

    address = st.text_area(
        "Address",
        value=profile.get("address", "")
    )

    col1, col2 = st.columns(2)

    with col1:
        city = st.text_input(
            "City",
            value=profile.get("city", "")
        )

    with col2:
        state = st.text_input(
            "State",
            value=profile.get("state", "")
        )

    pincode = st.text_input(
        "Pincode",
        value=profile.get("pincode", "")
    )

    save = st.form_submit_button(
        "💾 Save Changes",
        use_container_width=True
    )

# =====================================
# SAVE PROFILE
# =====================================

if save:

    # Basic Validation
    if full_name.strip() == "":
        st.error("Full Name is required.")

    elif phone and not phone.isdigit():
        st.error("Phone Number should contain only digits.")

    elif phone and len(phone) != 10:
        st.error("Phone Number must be 10 digits.")

    elif pincode and (not pincode.isdigit() or len(pincode) != 6):
        st.error("Pincode must be 6 digits.")

    else:

        result = update_profile(
            user.id,
            {
                "full_name": full_name,
                "phone": phone,
                "address": address,
                "city": city,
                "state": state,
                "pincode": pincode
            }
        )

        if result:
            st.success("✅ Profile Updated Successfully")
    
        else:
            st.error("Failed to update profile.")