from database.supabase import supabase

# ==============================
# PRODUCTS
# ==============================

def get_products():
    """Fetch all products."""
    try:
        response = (
            supabase
            .table("products")
            .select("*")
            .execute()
        )

        return response.data

    except Exception as e:
        print("Error fetching products:", e)
        return []


def get_product_by_id(product_id):
    """Fetch a single product."""
    try:
        response = (
            supabase
            .table("products")
            .select("*")
            .eq("id", product_id)
            .single()
            .execute()
        )

        return response.data

    except Exception as e:
        print("Error fetching product:", e)
        return None


# ==============================
# PROFILE
# ==============================

def get_profile(user_id):
    """Fetch logged-in user's profile."""
    try:
        response = (
            supabase
            .table("profiles")
            .select("*")
            .eq("id", user_id)
            .single()
            .execute()
        )

        return response.data

    except Exception as e:
        print("Error fetching profile:", e)
        return None


# ==============================
# WISHLIST
# ==============================

def add_to_wishlist(user_id, product_id):
    """Add a product to the user's wishlist."""
    try:
        # Check if already exists
        existing = (
            supabase
            .table("wishlist")
            .select("*")
            .eq("user_id", user_id)
            .eq("product_id", product_id)
            .execute()
        )

        if existing.data:
            return False

        supabase.table("wishlist").insert({
            "user_id": user_id,
            "product_id": product_id
        }).execute()

        return True

    except Exception as e:
        print("Wishlist Error:", e)
        return False

def get_user_wishlist(user_id):
    try:
        response = (
            supabase
            .table("wishlist")
            .select("""
                id,
                product_id,
                products (
                    id,
                    title,
                    description,
                    price,
                    location
                )
            """)
            .eq("user_id", user_id)
            .execute()
        )

        return response.data

    except Exception as e:
        print("Wishlist Error:", e)
        return []
