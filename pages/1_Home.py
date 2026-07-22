import streamlit as st
from utils.database import get_products, add_to_wishlist

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="UrbanShop",
    page_icon="🏠",
    layout="wide"
)

# -----------------------------
# Check Login
# -----------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/2_Login.py")
    st.stop()

# Logged-in User
user = st.session_state["user"]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏪 UrbanShop")
st.sidebar.write(f"👤 **{user.email}**")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/2_Login.py")

# -----------------------------
# Home Page
# -----------------------------
st.title("🏠 UrbanShop")
st.success(f"Welcome, **{user.email}**! 👋")

st.divider()

st.subheader("🛍️ Available Products")

# Fetch Products
products = get_products()

if products:
    for product in products:

        with st.container():

            st.markdown(f"## {product['title']}")
            st.write(product["description"])
            st.write(f"💰 **Price:** ₹{product['price']}")
            st.write(f"📍 **Location:** {product['location']}")

            col1, col2 = st.columns(2)

            # Wishlist Button
            with col1:
                if st.button("❤️ Wishlist", key=f"wish_{product['id']}"):

                    if add_to_wishlist(user.id, product["id"]):
                        st.success(f"{product['title']} added to Wishlist! ❤️")
                    else:
                        st.warning("Product is already in your Wishlist.")

            # Cart Button
            with col2:
                if st.button("🛒 Add to Cart", key=f"cart_{product['id']}"):
                    st.success(f"{product['title']} added to Cart! 🛒")

            st.divider()

else:
    st.info("No products available.")