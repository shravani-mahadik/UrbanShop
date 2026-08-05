import uuid
from database.supabase import supabase


def upload_product_image(uploaded_file):
    try:
        # Create a unique filename
        extension = uploaded_file.name.split(".")[-1]
        filename = f"{uuid.uuid4()}.{extension}"

        # Upload to Supabase Storage
        supabase.storage.from_("products").upload(
            filename,
            uploaded_file.getvalue(),
            {"content-type": uploaded_file.type}
        )

        # Get Public URL
        image_url = (
            supabase.storage
            .from_("products")
            .get_public_url(filename)
        )

        return image_url

    except Exception as e:
        print(e)
        return None