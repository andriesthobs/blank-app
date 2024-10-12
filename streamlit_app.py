import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase with Streamlit secrets
try:
    # Load credentials from Streamlit secrets
    firebase_credentials = st.secrets["firebase"]

    # Initialize Firebase only if it's not already initialized
    if not firebase_admin._apps:
        cred = credentials.Certificate(firebase_credentials)
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://soil-monitor-badbe-default-rtdb.firebaseio.com/'
        })
        st.success("Firebase initialized successfully!")

except ValueError as e:
    st.error(f"Invalid Firebase credentials: {e}")
    st.stop()  # Stop the app if Firebase fails to initialize

except KeyError:
    st.error("Firebase credentials are missing in Streamlit secrets.")
    st.stop()

except Exception as e:
    st.error(f"Failed to initialize Firebase: {e}")
    st.stop()

# Function to fetch data from Firebase
def fetch_data_from_firebase():
    try:
        ref = db.reference('soil_data')
        data = ref.get()
        if not data:
            st.warning("No data available in Firebase.")
            return None
        return data
    except Exception as e:
        st.error(f"Failed to fetch data: {e}")
        return None

# Function to process data into a DataFrame
def process_data(data):
    df = pd.DataFrame(data).T  # Transpose to get timestamps as rows

    # Convert timestamp to datetime
    if pd.api.types.is_numeric_dtype(df['timestamp']):
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
    else:
        df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

    # Convert percentage columns to numeric
    df['gravel_percentage'] = pd.to_numeric(df['gravel_percentage'], errors='coerce')
    df['sand_percentage'] = pd.to_numeric(df['sand_percentage'], errors='coerce')
    df['silt_percentage'] = pd.to_numeric(df['silt_percentage'], errors='coerce')

    # Drop rows with NaN values in key columns
    df = df.dropna(subset=['gravel_percentage', 'sand_percentage', 'silt_percentage'])

    return df

# Streamlit App Title
st.title("Soil Detection Dashboard")

# Fetch and process data from Firebase
data = fetch_data_from_firebase()
if data:
    df = process_data(data)

    # Plot 1: Line chart of soil types over time
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    ax1.plot(df['timestamp'], df['gravel_percentage'], label='Gravel', marker='o')
    ax1.plot(df['timestamp'], df['sand_percentage'], label='Sand', marker='s')
    ax1.plot(df['timestamp'], df['silt_percentage'], label='Silt', marker='^')
    ax1.set_xlabel("Timestamp")
    ax1.set_ylabel("Soil Percentage (%)")
    ax1.set_title("Soil Types Detected Over Time")
    ax1.legend()

    # Prepare data for the bar plot
    df['Date_str'] = df['timestamp'].dt.strftime('%d-%m-%Y %H:%M:%S')
    df_melted = df.melt(id_vars=['Date_str'], 
                        value_vars=['gravel_percentage', 'sand_percentage', 'silt_percentage'])

    # Plot 2: Bar chart of soil percentages by date
    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.barplot(x='Date_str', y='value', hue='variable', data=df_melted, palette='Set3', ax=ax2)
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Soil Percentage (%)")
    ax2.set_title("Soil Detection Dates")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)

    # Display the plots in Streamlit columns
    SoilDect, SoilDate = st.columns(2)

    with SoilDect:
        st.subheader("Soil Types Detected")
        st.pyplot(fig1)

    with SoilDate:
        st.subheader("Soil Detection Dates")
        st.pyplot(fig2)
else:
    st.warning("No data available to display.")
