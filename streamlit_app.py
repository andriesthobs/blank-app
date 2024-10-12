import streamlit as st
import firebase_admin
from firebase_admin import credentials, db

# Verify Firebase credentials from Streamlit secrets
try:
    firebase_credentials = st.secrets["firebase"]
    st.write("Firebase credentials loaded successfully.")

    # Initialize Firebase only if it's not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://soil-monitor-badbe-default-rtdb.firebaseio.com/'
        })
        st.success("Firebase initialized successfully!")

    # Fetch a small test dataset
    ref = db.reference('soil_data')
    data = ref.get()
    st.write("Data fetched successfully:", data)

except Exception as e:
    st.error(f"Error: {e}")
