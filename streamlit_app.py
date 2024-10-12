import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Load Firebase credentials from Streamlit secrets
firebase_credentials = st.secrets["firebase"]

# Initialize Firebase app
cred = credentials.Certificate(firebase_credentials)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://soil-monitor-badbe-default-rtdb.firebaseio.com/'
})

# Test database access
st.write("Firebase connected successfully.")

# Fetch data to confirm connection
ref = db.reference('soil_data')
data = ref.get()

if data:
    st.write("Fetched Data:", data)
else:
    st.write("No data available.")
