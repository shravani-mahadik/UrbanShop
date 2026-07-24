import streamlit as st
from database.supabase import supabase

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="My Cart",
    page_icon="🛒",
    layout="wide"
)

# -----------------------------
# Check Login
# -----------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
    st.stop()

user = st.session_state["user"]

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("🏪 UrbanShop")
st.sidebar.write(f"👤 **{user.email}**")

if st.sidebar.button("🚪 Logout"):
    st.session_state.clear()
    st.switch_page("pages/1_Login.py")

# -----------------------------
# Cart Page
# -----------------------------
st.title("🛒 My Cart")

total = 0

try:
    cart = (
        supabase.table("cart")
        .select("*")
        .eq("user_id", user.id)
        .execute()
    )

    if cart.data:

        for item in cart.data:

            product = (
                supabase.table("products")
                .select("*")
                .eq("id", item["product_id"])
                .single()
                .execute()
            )

            p = product.data

            subtotal = p["price"] * item["quantity"]
            total += subtotal

            with st.container():

                st.subheader(p["title"])
                st.write(p["description"])

                st.write(f"💰 Price: ₹{p['price']}")
                st.write(f"📦 Quantity: {item['quantity']}")
                st.write(f"💵 Subtotal: ₹{subtotal}")

                if st.button("❌ Remove", key=f"remove_{item['id']}"):

                    supabase.table("cart")\
                        .delete()\
                        .eq("id", item["id"])\
                        .execute()

                    st.success("Removed from Cart")
                    st.rerun()

                st.divider()

        st.markdown("## -------------------------")
        st.markdown(f"## 💰 Total : ₹{total}")

        if st.button("Proceed to Checkout"):
            st.success("Checkout feature coming soon...")

    else:
        st.info("Your cart is empty.")

except Exception as e:
    st.error(e)