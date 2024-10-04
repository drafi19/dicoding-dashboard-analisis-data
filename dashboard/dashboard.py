import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')




def create_rfm_df(df):
    rfm_df = df.groupby('customer_unique_id').agg({
        'order_purchase_timestamp': 'max',
        'order_id': 'nunique',
        'price_y': 'sum'
    }).sort_values(by='order_id', ascending=False)
    
    rfm_df.columns = ['recency', 'frequency', 'monetary']

    rfm_df['recency'] = rfm_df['recency'].dt.date
    recent_date = df['order_purchase_timestamp'].dt.date.max()
    rfm_df['recency'] = rfm_df['recency'].apply(lambda x: (recent_date - x).days)

    return rfm_df


def create_bycategory_df(df):
    bycategory_df = df.groupby('product_category_name_english').agg({
        'product_id_y': 'count',
        'price_y': 'sum'
    }).sort_values(by='price_y', ascending=False)

    bycategory_df.columns = ['total_order', 'total_revenue']

    return bycategory_df



# Load data
all_df = pd.read_csv('all_df.csv')

# Order by date
datetime_columns = ["order_purchase_timestamp"]
all_df.sort_values(by="order_purchase_timestamp", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
  
# Create filter component
min_date = all_df["order_purchase_timestamp"].min()
max_date = all_df["order_purchase_timestamp"].max()
 
with st.sidebar:
    #Menambahkan Judul
    st.title("Filter Waktu")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
# Main df yang telah difilter
main_df = all_df[(all_df["order_purchase_timestamp"] >= str(start_date)) & 
                 (all_df["order_purchase_timestamp"] <= str(end_date))]

rfm_df = create_rfm_df(main_df)
bycategory_df = create_bycategory_df(main_df)


st.header("Dashboard Submission - Amin Afif Rafi\'i")



# Item paling laris dan tidak laris
st.subheader('Kategori Item Paling Laku dan Paling Tidak Laku')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='product_category_name_english', y='total_order', data=bycategory_df.sort_values(by='total_order', ascending=False).head(5),hue="product_category_name_english", palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Kategori', fontsize=30)
ax[0].set_title('Best Performing Products', loc='center', fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x="product_category_name_english", y="total_order", data=bycategory_df.sort_values(by="total_order", ascending=True).head(5),hue="product_category_name_english", palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Kategori", fontsize=30)
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)


# Item paling menghasilkan dan kurang menghasilkan
st.subheader('Kategori Item dengan Pendapatan Tertinggi dan Terendah')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(x='product_category_name_english', y='total_revenue', data=bycategory_df.sort_values(by='total_revenue', ascending=False).head(5),hue="product_category_name_english", palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel('Kategori', fontsize=30)
ax[0].set_title('Best Performing Products', loc='center', fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=20)

sns.barplot(x="product_category_name_english", y="total_revenue", data=bycategory_df.sort_values(by="total_revenue", ascending=True).head(5),hue="product_category_name_english", palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel("Kategori", fontsize=30)
ax[1].set_title("Worst Performing Product", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)
st.caption('Sumbu Y di chart kiri dalam satuan jutaan')



# RFM Analisi
st.subheader('Performa RFM (Top 5)')

col1, col2, col3 = st.columns(3)

with col1:
    avg_recency = round(rfm_df["recency"].mean(), 1)
    st.metric("Average Recency (days)", avg_recency)
with col2:
    avg_frequency = round(rfm_df["frequency"].mean(), 2)
    st.metric("Average Frequency", avg_frequency)
with col3:
    avg_currency = format_currency(rfm_df["monetary"].mean(), 'BRL', locale='pt_BR')
    st.metric("Average Monetary", avg_currency)

fig, ax = plt.subplots(nrows=3, ncols=1, figsize=(30, 50))

colors = ["#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4", "#72BCD4"]

sns.barplot(y="recency", x="customer_unique_id", data=rfm_df.sort_values(by="recency", ascending=True).head(5), palette=colors, ax=ax[0])
ax[0].set_ylabel(None)
ax[0].set_xlabel(None)
ax[0].set_title("Recency", loc="center", fontsize=50)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=15)

sns.barplot(y="frequency", x="customer_unique_id", data=rfm_df.sort_values(by="frequency", ascending=False).head(5), palette=colors, ax=ax[1])
ax[1].set_ylabel(None)
ax[1].set_xlabel(None)
ax[1].set_title("Frequency", loc="center", fontsize=50)
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=15)

sns.barplot(y="monetary", x="customer_unique_id", data=rfm_df.sort_values(by="monetary", ascending=False).head(5), palette=colors, ax=ax[2])
ax[2].set_ylabel(None)
ax[2].set_xlabel(None)
ax[2].set_title("Monetary", loc="center", fontsize=50)
ax[2].tick_params(axis='y', labelsize=35)
ax[2].tick_params(axis='x', labelsize=15)

st.pyplot(fig)

