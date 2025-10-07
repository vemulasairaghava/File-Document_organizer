from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

SUPABASE_URL = os.getenv("SUPABASE_URL", "https://ywybifmunuyuwqhbbmba.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "YOUR_SUPABASE_KEY")

# Create Supabase client
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
