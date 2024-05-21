import firebase_admin
from firebase_admin import credentials

# Initialize Firebase with the service account key file
cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred)
