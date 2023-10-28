import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
from babel.numbers import format_currency
import calendar

sns.set_theme(style="darkgrid")

pd.options.display.max_rows = None
pd.options.display.max_columns = None

st.set_page_config(layout='wide')
st.header(':bar_chart: Dashboard Brazilian E-Commerce', divider='blue', anchor='center')

df = pd.read_csv('main_data.csv')
all_data = df.copy()

# ------------------side bar------------------

# Menambahkan Logo
st.sidebar.image('https://res-2.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_256,w_256,f_auto,q_auto:eco/h8ccwg5vhjcoqu1qfuwv')

# Buat sidebar untuk filter kota
st.sidebar.header('Filter Here:')
cities = all_data['customer_city'].unique()
cities = ['Select All'] + list(cities)  # Tambahkan opsi "Select All"
city = st.sidebar.selectbox("Pilih kota:", options=cities)

# Filter data berdasarkan kota yang dipilih
if city == 'Select All':
    filtered_data = all_data  # Jika "Select All" dipilih, tampilkan semua data
else:
    filtered_data = all_data[all_data['customer_city'] == city]

# Buat sidebar untuk filter tahun
years = all_data['year'].unique()
years = ['Select All'] + list(years)  # Tambahkan opsi "Select All"
year = st.sidebar.selectbox("Pilih tahun:", options=years)

# Filter data berdasarkan tahun yang dipilih
if year == 'Select All':
    filtered_data = filtered_data  # Jika "Select All" dipilih, tampilkan semua data
else:
    filtered_data = filtered_data[filtered_data['year'] == year]

# Daftar nama bulan
bulan = [calendar.month_name[i] for i in range(1, 13)]

# Buat sidebar untuk filter bulan dengan format nama bulan
months = all_data['month'].unique()
months = ['Select All'] + bulan  # Tambahkan opsi "Select All" dan nama bulan
selected_month = st.sidebar.selectbox("Pilih bulan:", options=months)

# Filter data berdasarkan bulan yang dipilih
if selected_month == 'Select All':
    filtered_data = filtered_data  # Jika "Select All" dipilih, tampilkan semua data
else:
    month_index = bulan.index(selected_month) + 1  # Konversi nama bulan menjadi indeks bulan
    filtered_data = filtered_data[filtered_data['month'] == month_index]

# Buat sidebar untuk status pembayaran
payment_status = all_data['payment_type'].unique()
payment_status = ['Select All'] + list(payment_status)  # Tambahkan opsi "Select All"
payment = st.sidebar.selectbox("Pilih status pembayaran:", options=payment_status)

# Filter data berdasarkan status pembayaran yang dipilih
if payment == 'Select All':
    filtered_data = filtered_data  # Jika "Select All" dipilih, tampilkan semua data
else:
    filtered_data = filtered_data[filtered_data['payment_type'] == payment]

# membuat watermark
st.sidebar.info('Aditya Setyo Budi')
st.sidebar.info('adityasetyo7@gmail.com')
# st.sidebar.info('Id Dicoding: aditya_sb')

# KPI Dashboard
total_sales = round(filtered_data['payment_value'].sum(), 2)
average_rating = round(filtered_data['review_score'].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sales = round(filtered_data['payment_value'].mean(),2)
total_customers = filtered_data['customer_id'].nunique()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.subheader('Total Sales')
    st.subheader(f"BRL :orange[R$ {total_sales:,}]")
with col2:
    st.subheader('Average Rating')
    st.subheader(f'{average_rating} {star_rating}')
with col3:
    st.subheader('Average Transaction')
    st.subheader(f"BRL :orange[R$ {average_sales:,}]")
with col4:
    st.subheader('Total Customers')
    st.subheader(f"{total_customers:,}")

st.markdown("""---""")


st.subheader(":chart_with_upwards_trend: Total Revenue per Year and Month")
# mencari revenue setiap tahun
revenue_year = filtered_data.groupby(by=['year'])[['payment_value']].sum().sort_values(by='payment_value', ascending=False).reset_index()
# visualisasi total revenue setiap tahun
col1, col2,= st.columns(2)

with col1:
    fig = px.bar(revenue_year, x='year', y='payment_value', labels={'x': 'Tahun', 'y': 'Total Revenue'}, 
                 text_auto=True, 
                 title='Total Revenue per Year')
    fig.update_layout(xaxis_title='Tahun', yaxis_title='Total Revenue')
    st.plotly_chart(fig)
with col2:
# Monthly Revenue
    monthly_revenue = filtered_data.groupby(['month', 'year'])['payment_value'].mean().reset_index()

    # visualisasi monthly revenue
    fig = px.line(monthly_revenue, x='month', y='payment_value', labels={'x': 'Bulan', 'y': 'Total Revenue'}, 
                  title='Total Revenue per Month',
                  color='year')
    fig.update_layout(xaxis_title='Bulan', yaxis_title='Total Revenue')
    st.plotly_chart(fig)

st.markdown("""---""")

st.subheader(":bar_chart: Top Selling Products")

col1, col2 = st.columns(2)

# Top Selling Products by order
with col1:
    top_products = filtered_data['product_category_name_english'].value_counts().head(5)
    fig1 = px.bar(top_products, x=top_products.values, y=top_products.index, color=top_products.index,
                 title='Top Selling Products by Order', text=top_products.values,
                 labels={'x': 'Number of Orders', 'y': 'Product Category'})
    st.plotly_chart(fig1)

# Top Worst Selling Products by order
with col2:
    worst_products = filtered_data['product_category_name_english'].value_counts().tail(5)
    fig2 = px.bar(worst_products, x=worst_products.values, y=worst_products.index, color=worst_products.index,
                 title='Top Worst Selling Products by Order', text=worst_products.values,
                 labels={'x': 'Number of Orders', 'y': 'Product Category'})
    st.plotly_chart(fig2)

st.markdown("""---""")

st.subheader(":chart_with_upwards_trend: Total Revenue per City")

col1, col2 = st.columns(2)

# top 5 cities by revenue
with col1:
    top_cities = filtered_data.groupby('customer_city')['payment_value'].sum().sort_values(ascending=False).head(5)
    fig = px.bar(top_cities, x=top_cities.values, y=top_cities.index, color=top_cities.index,
                 title='Top 5 Cities by Revenue', text=top_cities.values, labels={'x': 'Number of Orders', 'y': 'City'})
    st.plotly_chart(fig)

# bottom 5 cities by revenue
with col2:
    bottom_cities = filtered_data.groupby('customer_city')['payment_value'].sum().sort_values(ascending=False).tail(5)
    fig = px.bar(bottom_cities, x=bottom_cities.values, y=bottom_cities.index, color=bottom_cities.index,
                 title='Bottom 5 Cities by Revenue', text=bottom_cities.values, labels={'x': 'Number of Orders', 'y': 'City'})
    st.plotly_chart(fig)

st.markdown("""---""")

st.subheader(":bar_chart: Payment Methods")

col1, col2 = st.columns(2)

# Payment Methods
with col1:
    fig = px.pie(filtered_data, names='payment_type', title='Payment Methods')
    st.plotly_chart(fig)

with col2:
    # total payment_type by rata-rata payment_value
    payment_type = filtered_data.groupby('payment_type')['payment_value'].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(payment_type, x='payment_type', y='payment_value',
                 color='payment_type',
                 title='Average Revenue by Payment Type',
                 text=round(payment_type['payment_value'], 2),
                 labels={'x': 'Payment Type', 'y': 'Average Payment Value'})
    st.plotly_chart(fig)

st.markdown("""---""")

st.subheader(":bar_chart: Status Pengiriman dan Tingkat Kepuasan Pelanggan")

col1, col2 = st.columns(2)

with col1:
    # Status Pengiriman
    fig = px.pie(filtered_data, names='shipping_deliveryrate', title='Status Pengiriman')
    st.plotly_chart(fig)

with col2:
    # Tingkat Kepuasan Pelanggan
    fig = px.pie(filtered_data, names='review_score', title='Tingkat Kepuasan Pelanggan')
    st.plotly_chart(fig)




st.markdown("""---""")

st.subheader(":chart_with_upwards_trend: RFM Analysis")

# RFM Analysis
# Pastikan kolom 'order_purchase_timestamp' adalah tipe data datetime
all_data['order_purchase_timestamp'] = pd.to_datetime(all_data['order_purchase_timestamp'])

# Hitung tanggal terakhir
recent_date = all_data['order_purchase_timestamp'].dt.date.max()

# Lanjutkan dengan perhitungan RFM
rfm_df = filtered_data.groupby(by='customer_unique_id', as_index=False).agg({
    'order_purchase_timestamp': 'max',
    'order_id': 'nunique',
    'payment_value': 'sum'
})

rfm_df.columns = ['customer_unique_id', 'max_order_timestamp', 'frequency', 'monetary']
rfm_df['max_order_timestamp'] = pd.to_datetime(rfm_df['max_order_timestamp'])
rfm_df['max_order_timestamp'] = rfm_df['max_order_timestamp'].dt.date

rfm_df['recency'] = rfm_df['max_order_timestamp'].apply(lambda x: (recent_date - x).days)
rfm_df.drop('max_order_timestamp', axis=1, inplace=True)


col1, col2, col3 = st.columns(3)

with col1:
    # By Recency
    fig = px.bar(rfm_df.sort_values('recency', ascending=True).head(5), x='recency', y='customer_unique_id', text='recency', title='Recency')
    st.plotly_chart(fig)

with col2:
    # By Frequency
    fig = px.bar(rfm_df.sort_values('frequency', ascending=True).head(5), x='frequency', y='customer_unique_id', text='frequency', title='Frequency')
    st.plotly_chart(fig)

with col3:
    # By Monetary
    fig = px.bar(rfm_df.sort_values('monetary', ascending=True).head(5), x='monetary', y='customer_unique_id', text='monetary', title='Monetary')
    st.plotly_chart(fig)

st.markdown("""---""")
st.subheader("Kesimpulan")
st.write("Kesimpulan dari analisis ini adalah:")
st.write("- Setiap tahun pendapatan atau revenue perusahaan meningkat, menunjukan tren yang sangat positif. tahun 2018 adalah revenue tertinggi yaitu sebesar 2300648.55.")
st.write("- Sao Paulo memiliki jumlah customer yang jauh lebih banyak daripada kota-kota lainnya, dengan total 3757 customer yang bertansaksi.")
st.write("- Sao Paulo memiliki jumlah order yang paling tinggi di antara semua kota seller. Ini menunjukkan bahwa Sao Paulo adalah pusat aktivitas penjualan online yang signifikan di Brasil, dengan jumlah penjual dan transaksi yang tinggi.")
st.write("- pertumbuhan order atau trasaksi tinggi pada awal quarter seperti q1 dan q2 akan tetapi mengalami penurunan pada quarter q3 dan q4 dan penurunan sangat tinggi.")
st.write("- Berdasarkan analisis menggunakan rfm setidaknya ada bebera customer atau pelanggan yang berkontribusi ke monetary, frequency dan recency perusahaan.")
