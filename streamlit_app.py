import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Dummy information for Visualization
soil_data = {
    'Date': ['01-01-2024', '02-01-2024', '03-01-2024', '04-01-2024'],
    'Soil_Type_A': [10, 15, 8, 12],
    'Soil_Type_B': [5, 8, 6, 10],
    'Soil_Type_C': [7, 10, 9, 14]
}

# Convert to DataFrame
df = pd.DataFrame(soil_data)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

# Streamlit Title
st.title("Soil Detection Dashboard")

# Plotting Soil Types Detected Over Time
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Soil_Type_A'], mode='lines+markers', name='Soil Type A'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Soil_Type_B'], mode='lines+markers', name='Soil Type B'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Soil_Type_C'], mode='lines+markers', name='Soil Type C'))
fig1.update_layout(title='Soil Types Detected Over Time', xaxis_title='Date', yaxis_title='Soil Count')

# Preparing Data for Bar Plot
df['Date_str'] = df['Date'].dt.strftime('%d-%m-%Y')
df_melted = df.melt(id_vars=['Date_str'], value_vars=['Soil_Type_A', 'Soil_Type_B', 'Soil_Type_C'])

# Plotting Soil Detection Dates
fig2 = px.bar(df_melted, x='Date_str', y='value', color='variable', barmode='group', title='Soil Detection Dates')
fig2.update_layout(xaxis_title='Date', yaxis_title='Soil Count', xaxis_tickangle=-45)

# Creating Columns for Layout
SoilDect, SoilDate = st.columns(2)

with SoilDect:
    st.subheader("Soil Types Detected")
    st.plotly_chart(fig1)

with SoilDate:
    st.subheader("Soil Detection Dates")
    st.plotly_chart(fig2)

# Displaying Soil Images
st.subheader("Soil Images")
st.image("soil_image1.jpg", caption="Soil Type A", use_column_width=True)
st.image("soil_image2.jpg", caption="Soil Type B", use_column_width=True)
st.image("soil_image3.jpg", caption="Soil Type C", use_column_width=True)
