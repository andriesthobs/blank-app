import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import datetime
import os

firebase_credentials = os.getenv('FIREBASE_CREDENTIALS')

if firebase_credentials:
    cred = credentials.Certificate(json.loads(firebase_credentials))  # Load the credentials from environment
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://your-database-url.firebaseio.com'
    })
################################################################################################################
# Initialize Firebase app
#if not firebase_admin._apps:
#    cred = credentials.Certificate("soil-monitor.json")
#    firebase_admin.initialize_app(cred, {
#        'databaseURL': 'https://soil-monitor-badbe-default-rtdb.firebaseio.com/'
#    })
#################################################################################################################
# Function to fetch data from Firebase
def fetch_data_from_firebase():
    ref = db.reference('soil_data')
    data = ref.get()
    return data

# Function to process the data from Firebase
def process_data(data):
    # Create a DataFrame from the data
    df = pd.DataFrame(data).T  # Transpose to get dates as rows

    # Check if timestamp is numeric (Unix timestamp) or string
    if pd.api.types.is_numeric_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')  # Convert from Unix timestamp to datetime
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')  # Convert from string to datetime

    # Ensure that only numeric values are processed
    df['gravel_percentage'] = pd.to_numeric(df['gravel_percentage'], errors='coerce')
    df['sand_percentage'] = pd.to_numeric(df['sand_percentage'], errors='coerce')
    df['silt_percentage'] = pd.to_numeric(df['silt_percentage'], errors='coerce')

    # Drop any rows that contain NaN values in these percentage columns
    df = df.dropna(subset=['gravel_percentage', 'sand_percentage', 'silt_percentage'])

    return df

# Streamlit application
st.title("Soil Detection Dashboard")

# Fetch data from Firebase
data = fetch_data_from_firebase()

# Process the data
df = process_data(data)

# Adjusting figure sizes for both plots
fig1, ax1 = plt.subplots(figsize=(6, 4))  # Reduced size to fit better in Streamlit columns
ax1.plot(df['timestamp'], df['gravel_percentage'], label='Gravel', marker='o')
ax1.plot(df['timestamp'], df['sand_percentage'], label='Sand', marker='s')
ax1.plot(df['timestamp'], df['silt_percentage'], label='Silt', marker='^')
ax1.set_xlabel("Timestamp")
ax1.set_ylabel("Soil Percentage (%)")
ax1.set_title("Soil Types Detected Over Time")
ax1.legend()

# Melt data for bar plot
df['Date_str'] = df['timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')
df_melted = df.melt(id_vars=['Date_str'], value_vars=['gravel_percentage', 'sand_percentage', 'silt_percentage'])

# Adjusting figure size for bar chart as well
fig2, ax2 = plt.subplots(figsize=(6, 4))  # Reduced size for bar chart
sns.barplot(x='Date_str', y='value', hue='variable', data=df_melted, palette='Set3', ax=ax2)
ax2.set_xlabel("Date")
ax2.set_ylabel("Soil Percentage (%)")
ax2.set_title("Soil Detection Dates")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

# Layout in Streamlit
SoilDect, SoilDate = st.columns(2)

with SoilDect:
    st.subheader("Soil Types Detected")
    st.pyplot(fig1)

with SoilDate:
    st.subheader("Soil Detection Dates")
    st.pyplot(fig2)
