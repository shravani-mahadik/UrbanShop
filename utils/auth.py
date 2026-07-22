from database.supabase import supabase


def signup_user(full_name, email, password):
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        if response.user:
            supabase.table("profiles").insert({
                "id": str(response.user.id),
                "full_name": full_name,
                "role": "user"
            }).execute()

        return response

    except Exception as e:
        raise Exception(str(e))


def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        return response

    except Exception as e:
        raise Exception(str(e))