import streamlit as st
from database.supabase import supabase

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Wishlist",
    page_icon="❤️",
    layout="wide"
)

# -----------------------------
# Check Login
# -----------------------------
if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/2_Login.py")
    st.stop()

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
# Wishlist Page
# -----------------------------
st.title("❤️ My Wishlist")

try:
    # Get wishlist items
    wishlist = (
        supabase
        .table("wishlist")
        .select("*")
        .eq("user_id", user.id)
        .execute()
    )

    if wishlist.data:

        for item in wishlist.data:

            # Get product details
            product = (
                supabase
                .table("products")
                .select("*")
                .eq("id", item["product_id"])
                .single()
                .execute()
            )

            p = product.data

            with st.container():

                st.subheader(p["title"])
                st.write(p["description"])

                st.write(f"💰 **Price:** ₹{p['price']}")
                st.write(f"📍 **Location:** {p['location']}")

                if st.button("❌ Remove", key=f"remove_{item['id']}"):

                    supabase.table("wishlist") \
                        .delete() \
                        .eq("id", item["id"]) \
                        .execute()

                    st.success("Removed from Wishlist ❤️")
                    st.rerun()

                st.divider()

    else:
        st.info("Your wishlist is empty.")

except Exception as e:
    st.error(f"Error: {e}")