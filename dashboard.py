import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go

# Function to get list of cryptocurrencies
def get_crypto_list():
    url = 'https://api.coingecko.com/api/v3/coins/list'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Function to get historical price data
def get_crypto_history(coin_id):
    url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart?vs_currency=usd&days=30'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        prices = data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df[['date', 'price']]
    return pd.DataFrame()

st.title('Cryptocurrency Dashboard')

crypto_list = get_crypto_list()
crypto_names = [f"{c['name']} ({c['symbol']})" for c in crypto_list]
crypto_ids = [c['id'] for c in crypto_list]

selected = st.selectbox('Select a cryptocurrency:', options=range(len(crypto_names)), format_func=lambda x: crypto_names[x])
selected_id = crypto_ids[selected]

if selected_id:
    st.subheader(f"{crypto_names[selected]} Price Data")
    df = get_crypto_history(selected_id)
    currentPrice=df['price'][0] if not df.empty else 'N/A'
    st.write("Current Price (USD):",currentPrice)
    if not df.empty:
        #st.write(df)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines', name='Price'))
        fig.update_layout(title='Historical Price (Last 30 Days)', xaxis_title='Date', yaxis_title='Price (USD)')
        st.plotly_chart(fig)
    else:
        st.write('No data available.')
