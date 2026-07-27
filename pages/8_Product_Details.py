import streamlit as st
from utils.database import (
    get_product_by_id,
    add_to_wishlist,
    add_to_cart
)

st.set_page_config(
    page_title="Product Details",
    page_icon="🛍️",
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

# -----------------------------
# Product Check
# -----------------------------
if "selected_product" not in st.session_state:
    st.error("No product selected.")
    st.switch_page("pages/3_Home.py")
    st.stop()

product = get_product_by_id(
    st.session_state["selected_product"]
)

if not product:
    st.error("Product not found.")
    st.stop()

# -----------------------------
# Back Button
# -----------------------------
if st.button("⬅ Back to Home"):
    st.switch_page("pages/3_Home.py")

st.divider()

# -----------------------------
# Layout
# -----------------------------
col1, col2 = st.columns([1, 1])

with col1:

    if product["images"]:
        st.image(
            product["images"][0],
            use_container_width=True
        )

with col2:

    st.title(product["title"])

    st.write(product["description"])

    st.markdown(f"## ₹{product['price']:,.0f}")

    st.write(f"📍 {product['location']}")

    st.write("⭐⭐⭐⭐⭐ 4.5 (120 Reviews)")

    st.write("")

    if st.button("❤️ Add to Wishlist"):

        if add_to_wishlist(user.id, product["id"]):
            st.success("Added to Wishlist ❤️")
        else:
            st.info("Already in Wishlist")

    if st.button("🛒 Add to Cart"):

        if add_to_cart(user.id, product["id"]):
            st.success("Added to Cart 🛒")
        else:
            st.error("Failed to add to Cart")

    if product.get("reseller_link"):
        st.link_button(
            "🛍 Buy Now",
            product["reseller_link"]
        )