# Import library yang dibutuhkan
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from PIL import Image 

sns.set(style='dark')

# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='datetime').agg({
        "user_casual": "sum",
        "user_registered": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    return daily_rent_df

def create_byseason_df(df):
    byseason_df = df.groupby(by="season").count_total.sum().reset_index()
    
    return byseason_df

# Membaca dataset yang digunakan
day_df = pd.read_csv('main_data.csv')

day_df["datetime"] = pd.to_datetime(day_df["datetime"])
day_df.sort_values(by="datetime", inplace=True)
day_df.reset_index(inplace=True)

# Filter data
min_date = day_df["datetime"].min()
max_date = day_df["datetime"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    # Membuka gambar logo
    image = Image.open('logo.png')
    
    # Menampilkan logo
    st.image(image)
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = day_df[(day_df["datetime"] >= str(start_date)) & 
                (day_df["datetime"] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
season_rent_df = create_byseason_df(main_df)

# Visualisasi untuk Penyewaan Sepeda Berdasarkan Jenis User per Bulan Tahun 2011-2012
st.header('Bike-sharing Rental Dashboard')
st.subheader('Daily Rental')

col1, col2 = st.columns(2)

with col1:
    total_casual = daily_rent_df.user_casual.sum()
    st.metric("Total rent user casual", value=total_casual)

with col2:
    total_registered = daily_rent_df.user_registered.sum()
    st.metric("Total rent user registered", value=total_registered)

fig, ax = plt.subplots(figsize=(12, 6))

sns.lineplot(x='datetime', y='user_casual', data=main_df, marker='o', label='Casual', ax=ax)
sns.lineplot(x='datetime', y='user_registered', data=main_df, marker='o', label='Registered', ax=ax)
plt.xlabel('Date')
plt.ylabel('Total Count')
st.pyplot(fig)

# Visualisasi Penyewaan Sepeda berdasarkan Musim(Season)
st.subheader("Number of Customer by Season")

fig, ax = plt.subplots(figsize=(20, 10))

sns.barplot( 
        x="season",
        y="count_total",
        data=season_rent_df.sort_values(by="season", ascending=False),
        palette="coolwarm",
        ax=ax
    )

plt.xlabel("Season",fontsize=25)
plt.ylabel('Total Users',fontsize=25)
plt.xticks(range(0, 4), ['Springer', 'Summer', 'Fall', 'Winter'])
st.pyplot(fig)

st.caption('Copyright © MFA 2023')
