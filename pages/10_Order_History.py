import streamlit as st
from utils.database import get_user_orders, get_product_by_id

st.set_page_config(
    page_title="My Orders",
    page_icon="📦",
    layout="wide"
)

# Login check
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
    st.stop()

user = st.session_state["user"]

st.title("📦 My Orders")

orders = get_user_orders(user.id)

if not orders:
    st.info("You haven't placed any orders yet.")
    st.stop()

for order in orders:

    product = get_product_by_id(order["product_id"])

    if product is None:
        continue

    st.subheader(product["title"])

    st.write(f"💰 Price: ₹{product['price']:,}")
    st.write(f"📦 Quantity: {order['quantity']}")
    st.write(f"💵 Total: ₹{order['total_price']:,}")
    st.write(f"🚚 Status: {order['status']}")
    st.write(f"📍 Address: {order['address']}")
    st.write(f"📞 Phone: {order['phone']}")
    st.write(f"📅 Ordered At: {order['ordered_at']}")

    st.divider()