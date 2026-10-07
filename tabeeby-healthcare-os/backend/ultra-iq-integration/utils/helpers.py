"""Helpers for ultra-iq-integration"""
from datetime import datetime
import random, string
def generate_id(prefix=""):
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{suffix}" if prefix else suffix
def now_iso(): return datetime.utcnow().isoformat()
def now_timestamp(): return int(datetime.utcnow().timestamp())
