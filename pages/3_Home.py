import streamlit as st
from utils.database import (
    get_products,
    add_to_wishlist,
    add_to_cart
)

# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="UrbanShop",
    page_icon="🏠",
    layout="wide"
)

# ---------------------------------
# Login Check
# ---------------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")   # Change if your login page has a different name
    st.stop()

user = st.session_state["user"]

# ---------------------------------
# Sidebar
# ---------------------------------
st.sidebar.title("🏪 UrbanShop")
st.sidebar.write(f"👤 {user.email}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/1_Login.py")

# ---------------------------------
# Home
# ---------------------------------
st.title("🏪 UrbanShop")
st.write(f"Welcome **{user.email}** 👋")

st.divider()

# ---------------------------------
# Search
# ---------------------------------
search = st.text_input(
    "🔍 Search Products",
    placeholder="Search products..."
)

products = get_products()

if search:
    products = [
        p for p in products
        if search.lower() in p["title"].lower()
    ]

# ---------------------------------
# Products
# ---------------------------------
if products:

    cols = st.columns(3)

    for index, product in enumerate(products):

        with cols[index % 3]:

            with st.container(border=True):

                if product["images"]:
                    st.image(
                        product["images"][0],
                        width=250
                    )

                st.markdown(
                    f"""
                    <h2 style="height:80px;">
                    {product['title']}
                    </h2>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"""
                    <p style="height:50px;color:gray;">
                    {product['description']}
                    </p>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(
                    f"## 💰 ₹{product['price']:,.0f}"
                )

                st.write(f"📍 {product['location']}")
                st.write("⭐ 4.5 (120 Reviews)")

                col1, col2 = st.columns(2)

                with col1:
                    if st.button(
                        "❤️ Wishlist",
                        key=f"wish_{product['id']}"
                    ):
                        add_to_wishlist(user.id, product["id"])

                with col2:
                    if st.button(
                        "🛒 Add",
                        key=f"cart_{product['id']}"
                    ):
                        add_to_cart(user.id, product["id"])