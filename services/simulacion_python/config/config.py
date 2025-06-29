# config.py

from dotenv import load_dotenv
import os

load_dotenv()

THINGSBOARD_HOST = os.getenv("THINGSBOARD_HOST")
DEVICE_TOKEN = os.getenv("DEVICE_TOKEN")
TENANT_USER = os.getenv("TENANT_USER")
TENANT_PASSWORD = os.getenv("TENANT_PASSWORD")
