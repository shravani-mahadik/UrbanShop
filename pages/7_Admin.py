import streamlit as st
from database.supabase import supabase
from utils.storage import upload_product_image
from utils.database import get_profile

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Admin Dashboard",
    page_icon="🛠️",
    layout="wide"
)

# ==========================================
# LOGIN CHECK
# ==========================================

if "user" not in st.session_state:
    st.warning("Please login first.")
    st.switch_page("pages/1_Login.py")
    st.stop()

user = st.session_state["user"]

# ==========================================
# ADMIN CHECK
# ==========================================

profile = get_profile(user.id)

if profile is None:
    st.error("Profile not found.")
    st.stop()

if profile.get("role") != "admin":
    st.error("⛔ Access Denied")
    st.info("You are not authorized to access the Admin Dashboard.")
    st.stop()


st.title("🛠️ Admin Dashboard")

# ==========================================
# DASHBOARD STATS
# ==========================================

products_count = (
    supabase.table("products")
    .select("*", count="exact")
    .execute()
)

users_count = (
    supabase.table("profiles")
    .select("*", count="exact")
    .execute()
)

orders_count = (
    supabase.table("orders")
    .select("*", count="exact")
    .execute()
)

revenue = (
    supabase.table("orders")
    .select("total_price")
    .execute()
)

total_revenue = 0

if revenue.data:
    total_revenue = sum(
        order["total_price"]
        for order in revenue.data
    )

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("📦 Products", products_count.count)

with c2:
    st.metric("👥 Users", users_count.count)

with c3:
    st.metric("🛒 Orders", orders_count.count)

with c4:
    st.metric(
        "💰 Revenue",
        f"₹{total_revenue:,.0f}"
    )

st.divider()

# ==========================================
# FETCH CATEGORIES
# ==========================================

categories = (
    supabase.table("categories")
    .select("*")
    .execute()
)

category_map = {
    c["name"]: c["id"]
    for c in categories.data
}

# ==========================================
# ADD PRODUCT
# ==========================================

st.header("➕ Add Product")

with st.form("add_product"):

    title = st.text_input("Product Name")

    description = st.text_area("Description")

    price = st.number_input(
        "Price",
        min_value=0.0
    )

    category = st.selectbox(
        "Category",
        list(category_map.keys())
    )

    location = st.text_input("Location")

    uploaded_image = st.file_uploader(
        "Product Image",
        type=["jpg", "jpeg", "png"]
    )

    reseller_link = st.text_input(
        "Reseller Link"
    )

    submit = st.form_submit_button(
        "➕ Add Product"
    )

    if submit:

        image_url = ""

        if uploaded_image:
            image_url = upload_product_image(
                uploaded_image
            )

        response = (
            supabase
            .table("products")
            .insert({
                "title": title,
                "description": description,
                "price": price,
                "category_id": category_map[category],
                "location": location,
                "images": [image_url] if image_url else [],
                "reseller_link": reseller_link,
                "created_by": user.id
            })
            .execute()
        )

        if response.data:
            st.success("✅ Product Added")
            st.rerun()

st.divider()

# ==========================================
# MANAGE PRODUCTS
# ==========================================

st.header("📋 Manage Products")

products = (
    supabase
    .table("products")
    .select("""
        *,
        categories(name)
    """)
    .order("id")
    .execute()
)

if not products.data:
    st.info("No products found.")

else:

    for product in products.data:

        st.divider()

        category_name = "N/A"

        if product.get("categories"):
            category_name = product["categories"]["name"]

        col1, col2 = st.columns([4,1])

        with col1:

            if product.get("images") and len(product["images"]) > 0:
                st.image(
                    product["images"][0],
                    width=180
                )

            st.subheader(product["title"])

            st.write(product["description"])

            st.write(f"💰 Price : ₹{product['price']:,.0f}")

            st.write(f"📂 Category : {category_name}")

            st.write(f"📍 Location : {product['location']}")

        with col2:

            if st.button(
                "✏️ Edit",
                key=f"edit_{product['id']}"
            ):
                st.session_state["edit_product"] = product["id"]

            if st.button(
                "❌ Delete",
                key=f"delete_{product['id']}"
            ):

                (
                    supabase
                    .table("products")
                    .delete()
                    .eq("id", product["id"])
                    .execute()
                )

                st.success("Product Deleted Successfully")

                st.rerun()

        # ==================================
        # SHOW EDIT FORM
        # ==================================

        if st.session_state.get("edit_product") == product["id"]:

            st.info("Editing Product")

            st.session_state["current_product"] = product

            with st.form(f"edit_form_{product['id']}"):

                 new_title = st.text_input(
                    "Product Name",
                     value=product["title"]
                )

                 new_description = st.text_area(
                   "Description",
                   value=product["description"]
                 )

                 new_price = st.number_input(
                    "Price",
                    min_value=0.0,
                    value=float(product["price"])
                )

                 category_names = list(category_map.keys())

                 current_category = category_name

                 default_index = 0

                 if current_category in category_names:
                    default_index = category_names.index(current_category)

                 new_category = st.selectbox(
                     "Category",
                     category_names,
                     index=default_index
                )

                 new_location = st.text_input(
                    "Location",
                    value=product["location"]
                )

    # Current Image
                 current_image = ""

                 if product.get("images") and len(product["images"]) > 0:

                    current_image = product["images"][0]

                    st.image(
                    current_image,
                    width=180
                     )

                 uploaded_new_image = st.file_uploader(
                    "Upload New Image",
                    type=["jpg", "jpeg", "png"],
                    key=f"upload_{product['id']}"
                    )

                 new_reseller = st.text_input(
                    "Reseller Link",
                    value=product.get("reseller_link", "")
                    )

                 col_save, col_cancel = st.columns(2)

                 with col_save:
                    update = st.form_submit_button("💾 Update")

                 with col_cancel:
                    cancel = st.form_submit_button("❌ Cancel")


                 if update:

                    updated_image = current_image

                    if uploaded_new_image:
                        uploaded_url = upload_product_image(uploaded_new_image)
                        if uploaded_url:
                            updated_image = uploaded_url

                    (
                        supabase
                        .table("products")
                        .update({
                            "title": new_title,
                            "description": new_description,
                            "price": new_price,
                            "category_id": category_map[new_category],
                            "location": new_location,
                            "images": [updated_image] if updated_image else [],
                            "reseller_link": new_reseller
                        })
                        .eq("id", product["id"])
                        .execute()
                    )

                    st.success("✅ Product Updated Successfully")
                    st.session_state.pop("edit_product", None)
                    st.rerun()

            if cancel:
                st.session_state.pop("edit_product", None)
                st.rerun()