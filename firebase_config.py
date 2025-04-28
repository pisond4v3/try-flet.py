import os
import firebase_admin
from firebase_admin import credentials, firestore
import requests
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Firebase Admin SDK for Firestore
try:
    cred_path = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY", "serviceAccountKey.json")
    if not os.path.exists(cred_path):
        raise FileNotFoundError(f"Service account key file not found at: {cred_path}")
    cred = credentials.Certificate(cred_path)
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    logger.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
    raise

# Firebase Authentication REST API configuration
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY", "AIzaSyC1G4tnb9PWS8NQK3IcyjCZFoWx-rUmxk0")
if not FIREBASE_API_KEY or "YOUR_API_KEY_HERE" in FIREBASE_API_KEY:
    logger.error("Firebase API key is missing or invalid")
    raise ValueError("Firebase API key is required for authentication")

# Helper functions for Firebase Authentication REST API
def sign_in_with_email_and_password(email, password):
    """Sign in a user with email and password using Firebase REST API."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["localId"]
    except requests.RequestException as e:
        logger.error(f"Authentication failed: {str(e)}")
        raise Exception(response.json().get("error", {}).get("message", str(e)))

def create_user_with_email_and_password(email, password):
    """Create a new user with email and password using Firebase REST API."""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()["localId"]
    except requests.RequestException as e:
        logger.error(f"User creation failed: {str(e)}")
        raise Exception(response.json().get("error", {}).get("message", str(e)))

logger.info("Firebase Admin SDK and Auth REST API initialized successfully")