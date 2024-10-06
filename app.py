import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


df=pd.read_csv('ImportsExportsDataset.csv')
my_sample=df.sample(n=3001, random_state=55042) 

# Page configuration
st.set_page_config(
    page_title="Import-Export Dashboard",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page background color and custom CSS
page_bg_color = """
    <style>
    body {
        background-color: #e8f5e9;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
    }
    .metric-box {
        padding: 15px;
        margin: 5px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
    }
    .metric-title {
        font-size: 16px;
        font-weight: bold;
        color: #333333;
    }
    .metric-value {
        font-size: 20px;
        color: #007bff;
    }
    .metric-delta {
        color: #ff6b6b;
    }
    </style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title('📦 Import-Export Dashboard')
# Assuming my_sample is your dataset
my_sample['Date'] = pd.to_datetime(my_sample['Date'], dayfirst=True)
monthly_value = my_sample.resample('M', on='Date')['Value'].sum()

# Streamlit app
st.title('Monthly Transaction Trends')

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(monthly_value.index, monthly_value.values, marker='o', linestyle='-', color='blue')
ax.set_title('Total Monthly Transaction Value')
ax.set_xlabel('Month')
ax.set_ylabel('Total Value')
ax.grid(True)
plt.tight_layout()

st.pyplot(fig)


country_value = my_sample.groupby('Country')['Value'].sum().sort_values(ascending=False)

# Streamlit app
st.title('Top Countries by Total Transaction Value')

top_n = st.slider('Select number of top countries to display:', min_value=5, max_value=20, value=10)
fig, ax = plt.subplots(figsize=(10, 6))
country_value.head(top_n).plot(kind='bar', color='skyblue', ax=ax)
ax.set_title('Top Countries by Total Transaction Value')
ax.set_xlabel('Country')
ax.set_ylabel('Total Value')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


import seaborn as sns

# Streamlit app
st.title('Transaction Value Distribution by Product Category')

fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(x='Category', y='Value', data=my_sample, ax=ax)
ax.set_title('Transaction Value by Product Category')
ax.set_xlabel('Product Category')
ax.set_ylabel('Transaction Value')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


import_export_value = my_sample.groupby(['Country', 'Import_Export'])['Value'].sum().unstack().fillna(0)

# Streamlit app
st.title('Import vs. Export Value by Country')

fig, ax = plt.subplots(figsize=(12, 8))
import_export_value.plot(kind='bar', stacked=True, ax=ax, color=['orange', 'green'])
ax.set_title('Import vs. Export Value per Country')
ax.set_xlabel('Country')
ax.set_ylabel('Total Value')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


shipping_value = my_sample.groupby('Shipping_Method')['Value'].mean().sort_values(ascending=False)

# Streamlit app
st.title('Shipping Method vs. Average Transaction Value')

fig, ax = plt.subplots(figsize=(10, 6))
shipping_value.plot(kind='bar', color='lightcoral', ax=ax)
ax.set_title('Average Transaction Value by Shipping Method')
ax.set_xlabel('Shipping Method')
ax.set_ylabel('Average Value')
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


from scipy.stats import linregress

# Scatter plot with regression line
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Weight', y='Value', data=my_sample, alpha=0.5, color='blue', ax=ax)

# Regression line
slope, intercept, r_value, p_value, std_err = linregress(my_sample['Weight'], my_sample['Value'])
ax.plot(my_sample['Weight'], slope * my_sample['Weight'] + intercept, color='red', linestyle='--')
ax.set_title('Weight vs. Transaction Value with Regression Line')
ax.set_xlabel('Weight')
ax.set_ylabel('Transaction Value')
plt.tight_layout()

st.title('Weight vs. Transaction Value Analysis')
st.pyplot(fig)
