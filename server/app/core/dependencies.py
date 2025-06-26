from .config import settings
from supabase import create_client, Client
from functools import lru_cache

@lru_cache()
def get_supabase() -> Client:
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)