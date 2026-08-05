import os
import streamlit as st
from dotenv import load_dotenv
from supabase import create_client

# Load local .env (for local development)
load_dotenv()

# Use Streamlit Secrets if available, otherwise use .env
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL"))
SUPABASE_KEY = st.secrets.get(
    "SUPABASE_PUBLISHABLE_KEY",
    os.getenv("SUPABASE_PUBLISHABLE_KEY")
)

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)