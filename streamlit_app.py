import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

#Dummy information for Visualization
soil_data = {
    'Date': ['01-01-2023', '02-01-2023', '03-01-2023', '04-01-2023'],
    'Soil_Type_A': [10, 15, 8, 12],
    'Soil_Type_B': [5, 8, 6, 10],
    'Soil_Type_C': [7, 10, 9, 14]
}

df = pd.DataFrame(soil_data)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

st.title("Soil Detection Dashboard")

#st.subheader("Soil Types Detected")
fig1, ax1 = plt.subplots(figsize=(8, 6))
ax1.plot(df['Date'], df['Soil_Type_A'], label='Soil Type A', marker='o')
ax1.plot(df['Date'], df['Soil_Type_B'], label='Soil Type B', marker='s')
ax1.plot(df['Date'], df['Soil_Type_C'], label='Soil Type C', marker='^')
ax1.set_xlabel("Date")
ax1.set_ylabel("Soil Count")
ax1.set_title("Soil Types Detected Over Time")
ax1.legend()
#st.pyplot(fig1)

#st.subheader("Soil Detection Dates")
df['Date_str'] = df['Date'].dt.strftime('%d-%m-%Y')
df_melted = df.melt(id_vars=['Date_str'], value_vars=['Soil_Type_A', 'Soil_Type_B', 'Soil_Type_C'])
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x='Date_str', y='value', hue='variable', data=df_melted, palette='Set3', ax=ax2)
ax2.set_xlabel("Date")
ax2.set_ylabel("Soil Count")
ax2.set_title("Soil Detection Dates")
ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
#.pyplot(fig2)


SoilDect,SoilDate = st.columns(2)

with SoilDect :
    st.subheader("Soil Types Detected")
    st.pyplot(fig1)

with SoilDate :
    st.subheader("Soil Detection Dates")
    st.pyplot(fig2)    


st.subheader("Soil Images")
st.image("soil_image1.jpg", caption="Soil Type A", use_column_width=True)
st.image("soil_image2.jpg", caption="Soil Type B", use_column_width=True)
st.image("soil_image3.jpg", caption="Soil Type C", use_column_width=True)
