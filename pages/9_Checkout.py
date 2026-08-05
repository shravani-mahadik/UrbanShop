import streamlit as st

from database.supabase import supabase
from utils.database import (
    get_user_cart,
    place_order,
    clear_cart
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Checkout",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Login Check
# -----------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
    st.stop()

user = st.session_state["user"]

st.title("🛒 Checkout")

# -----------------------------
# Fetch Cart
# -----------------------------
cart_items = get_user_cart(user.id)

if not cart_items:
    st.info("Your cart is empty.")
    st.stop()

st.divider()

st.subheader("📍 Delivery Details")

address = st.text_area(
    "Delivery Address",
    placeholder="Enter your complete address"
)

phone = st.text_input(
    "Phone Number",
    placeholder="Enter your mobile number"
)

if st.button("✅ Place Order", use_container_width=True):

    if not address or not phone:
        st.error("Please fill in all details.")
        st.stop()

    success = True

    for item in cart_items:

        product = item["products"]

        order_data = {
            "user_id": user.id,
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "total_price": product["price"] * item["quantity"],
            "address": address,
            "phone": phone,
            "status": "Processing"
        }

        result = place_order(order_data)

        if result is None:
            success = False
            break

    if success:
        clear_cart(user.id)
        st.success("🎉 Order placed successfully!")
        st.balloons()

        st.switch_page("pages/10_Order_History.py")

    else:
        st.error("Failed to place order.")