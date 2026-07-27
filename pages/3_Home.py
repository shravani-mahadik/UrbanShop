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
    page_icon="🏪",
    layout="wide"
)

# ---------------------------------
# Login Check
# ---------------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
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
# Hero Banner
# ---------------------------------
st.markdown("""
<div style="
background: linear-gradient(90deg,#2563eb,#7c3aed);
padding:30px;
border-radius:15px;
color:white;
text-align:center;
margin-bottom:20px;
">
<h1>🛍️ UrbanShop</h1>
<p>Discover the best deals on Electronics, Fashion & Accessories</p>
</div>
""", unsafe_allow_html=True)

st.write(f"### 👋 Welcome, **{user.email}**")

st.divider()

# ---------------------------------
# Category Filter
# ---------------------------------

categories = [
    "All",
    "Electronics",
    "Laptops",
    "Accessories",
    "Fashion"
]

selected_category = st.selectbox(
    "📂 Category",
    categories
)# ---------------------------------
# Search Bar
# ---------------------------------
search = st.text_input(
    "🔍 Search Products",
    placeholder="Search products..."
)
# ---------------------------------
# Sort Products
# ---------------------------------

sort_option = st.selectbox(
    "↕️ Sort By",
    [
        "Default",
        "Price: Low to High",
        "Price: High to Low",
        "Name: A to Z",
        "Name: Z to A"
    ]
)
# ---------------------------------
# Get Products
# ---------------------------------
products = get_products()
#st.write(products)
category_map = {
    "Electronics": 1,
    "Laptops": 2,
    "Accessories": 3,
    "Fashion": 4
}

if selected_category != "All":
    products = [
        product
        for product in products
        if product["category_id"] == category_map[selected_category]
    ]

if search:
    products = [
        p for p in products
        if search.lower() in p["title"].lower()
    ]
# ---------------------------------
# Sorting Logic
# ---------------------------------

if sort_option == "Price: Low to High":
    products = sorted(
        products,
        key=lambda x: x["price"]
    )

elif sort_option == "Price: High to Low":
    products = sorted(
        products,
        key=lambda x: x["price"],
        reverse=True
    )

elif sort_option == "Name: A to Z":
    products = sorted(
        products,
        key=lambda x: x["title"].lower()
    )

elif sort_option == "Name: Z to A":
    products = sorted(
        products,
        key=lambda x: x["title"].lower(),
        reverse=True
    )
# ---------------------------------
# Product Cards

# ---------------------------------
if products:

    cols = st.columns(3)

    for index, product in enumerate(products):

        with cols[index % 3]:

            with st.container(border=True):

                # -----------------------------
                # Product Image
                st.markdown(
    """
    <span style="
        background:#ff9800;
        color:white;
        padding:4px 10px;
        border-radius:12px;
        font-size:12px;
        font-weight:bold;">
        ⭐ Best Seller
    </span>
    """,
    unsafe_allow_html=True
)               
                if product["images"]:
                    st.image(
                        product["images"][0],
                        width=260
                    )   
                
                # -----------------------------
                # Product Name
                # -----------------------------
                st.markdown(
                    f"""
                    <div style="height:60px;">
                        <h4>{product['title']}</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # -----------------------------
                # Description
                # -----------------------------
                st.markdown(
                    f"""
                    <div style="
                        height:45px;
                        color:gray;
                        font-size:14px;
                    ">
                        {product['description']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")
                # -----------------------------
                # Price
                
                # -----------------------------

                original_price = int(product["price"] * 1.25)

                st.markdown(
                    f"### 🟢 ₹{product['price']:,.0f}"
                )
                st.caption(f"~~₹{original_price:,.0f}~~   🔥 **20% OFF**")
                # -----------------------------
                # Location
                # -----------------------------
                st.write(f"📍 {product['location']}")

                # -----------------------------
                # Rating
                # -----------------------------
                st.markdown(
                    """
                    <span style="color:#f59e0b;font-size:18px;">
                        ★★★★★
                    </span>
                    <span style="color:gray;">
                        4.5 (120 Reviews)
                    </span>
                    """,
                    unsafe_allow_html=True
                )

                st.write("")
                

                # -----------------------------
                # Buttons
                # -----------------------------
                col1, col2, col3 = st.columns(3)

                with col1:
                     if st.button(
                         "❤️ Wishlist",
                         key=f"wish_{product['id']}"
               ):
                         result = add_to_wishlist(user.id, product["id"])

                         if result:
                           st.success("Added to Wishlist ❤️")
                         else:
                           st.info("Already in Wishlist")

                with col2:
                     if st.button(
                         "🛒 Add to cart",
                          key=f"cart_{product['id']}"
                ):
                          result = add_to_cart(user.id, product["id"])

                          if result:
                              st.success("Added to Cart 🛒")
                          else:
                               st.error("Failed to add product")

                with col3:
                      if st.button(
                       "👀 Details",
                       key=f"details_{product['id']}"
                ):
                         st.session_state["selected_product"] = product["id"]
                         st.switch_page("pages/8_Product_Details.py")
else:
    st.info("No products available.")