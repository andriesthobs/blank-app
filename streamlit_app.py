import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Access Firebase credentials from Streamlit secrets
firebase_credentials = st.secrets["firebase"]

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    try:
        # Create credentials using the secret values
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://soil-monitor-badbe-default-rtdb.firebaseio.com/'
        })
        st.success("Firebase initialized successfully!")
    except Exception as e:
        st.error(f"Failed to initialize Firebase: {e}")

# Function to fetch data from Firebase
def fetch_data_from_firebase():
    try:
        ref = db.reference('soil_data')
        data = ref.get()
        if not data:
            st.warning("No data found.")
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

# Function to process the data
def process_data(data):
    df = pd.DataFrame(data).T

    # Handle timestamp conversion
    if pd.api.types.is_numeric_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Convert percentages to numeric and drop NaN
    df[['gravel_percentage', 'sand_percentage', 'silt_percentage']] = df[
        ['gravel_percentage', 'sand_percentage', 'silt_percentage']
    ].apply(pd.to_numeric, errors='coerce')

    df = df.dropna(subset=['gravel_percentage', 'sand_percentage', 'silt_percentage'])
    return df

# Streamlit app
st.title("Soil Detection Dashboard")

# Fetch and process data
data = fetch_data_from_firebase()
if data:
    df = process_data(data)

    # Date range slider
    min_date, max_date = df['timestamp'].min(), df['timestamp'].max()
    date_range = st.slider("Select Date Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    df_filtered = df[(df['timestamp'] >= date_range[0]) & (df['timestamp'] <= date_range[1])]

    # Line plot: Soil Types Over Time
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(df_filtered['timestamp'], df_filtered['gravel_percentage'], label='Gravel', marker='o')
    ax1.plot(df_filtered['timestamp'], df_filtered['sand_percentage'], label='Sand', marker='s')
    ax1.plot(df_filtered['timestamp'], df_filtered['silt_percentage'], label='Silt', marker='^')
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Soil Percentage (%)")
    ax1.set_title("Soil Types Detected Over Time")
    ax1.legend()

    # Bar plot: Soil Detection Dates
    df_filtered['Date_str'] = df_filtered['timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')
    df_melted = df_filtered.melt(id_vars=['Date_str'], value_vars=['gravel_percentage', 'sand_percentage', 'silt_percentage'])

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='Date_str', y='value', hue='variable', data=df_melted, palette='Set3', ax=ax2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Soil Percentage (%)")
    ax2.set_title("Soil Detection Dates")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

    # Display plots in columns
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Soil Types Detected")
        st.pyplot(fig1)

    with col2:
        st.subheader("Soil Detection Dates")
        st.pyplot(fig2)
else:
    st.stop()
