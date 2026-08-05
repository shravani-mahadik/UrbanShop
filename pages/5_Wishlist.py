import streamlit as st
from database.supabase import supabase
from utils.database import add_to_cart

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
# Wishlist Page
# -----------------------------
st.title("❤️ My Wishlist")

try:
    wishlist = (
        supabase
        .table("wishlist")
        .select("*")
        .eq("user_id", user.id)
        .execute()
    )

    if wishlist.data:

        for item in wishlist.data:

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

                st.write(f"💰 **Price:** ₹{p['price']:,}")
                st.write(f"📍 **Location:** {p['location']}")

                # -----------------------------
                # Buttons
                # -----------------------------
                col1, col2 = st.columns(2)

                # Add to Cart
                with col1:
                    if st.button(
                        "🛒 Add to Cart",
                        key=f"cart_{item['id']}",
                        use_container_width=True
                    ):

                        success = add_to_cart(
                            user.id,
                            item["product_id"]
                        )

                        if success:
                            (
                                supabase
                                .table("wishlist")
                                .delete()
                                .eq("id", item["id"])
                                .execute()
                            )

                            st.success("Product moved to Cart 🛒")
                            st.rerun()
                        else:
                            st.error("Failed to add product to cart.")

                # Remove from Wishlist
                with col2:
                    if st.button(
                        "❌ Remove",
                        key=f"remove_{item['id']}",
                        use_container_width=True
                    ):

                        (
                            supabase
                            .table("wishlist")
                            .delete()
                            .eq("id", item["id"])
                            .execute()
                        )

                        st.success("Removed from Wishlist ❤️")
                        st.rerun()

                st.divider()

    else:
        st.info("❤️ Your wishlist is empty.")

except Exception as e:
    st.error(f"Error: {e}")