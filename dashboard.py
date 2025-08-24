import streamlit as st
import pandas as pd
import requests
import plotly.graph_objs as go

# Function to get list of cryptocurrencies
def get_crypto_list():
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []

# Function to get historical price data
def get_crypto_history(symbol):
    # Binance API returns up to 1000 candles, here we get daily candles for last 30 days
    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1d&limit=30'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Each kline: [Open time, Open, High, Low, Close, Volume, ...]
        df = pd.DataFrame(data, columns=[
            'open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time',
            'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume',
            'taker_buy_quote_asset_volume', 'ignore'])
        df['date'] = pd.to_datetime(df['open_time'], unit='ms')
        df['price'] = df['close'].astype(float)
        return df[['date', 'price']]
    return pd.DataFrame()

st.title('Cryptocurrency Dashboard')

crypto_list = get_crypto_list()
if len(crypto_list) == 0:
    st.error("Could not load cryptocurrency list from Binance API.")
else:
    # Static mapping for common symbols to names
    symbol_name_map = {
        'BTCUSDT': 'Bitcoin',
        'ETHUSDT': 'Ethereum',
        'BNBUSDT': 'Binance Coin',
        'ADAUSDT': 'Cardano',
        'XRPUSDT': 'Ripple',
        'SOLUSDT': 'Solana',
        'DOGEUSDT': 'Dogecoin',
        'DOTUSDT': 'Polkadot',
        'MATICUSDT': 'Polygon',
        'LTCUSDT': 'Litecoin',
        'TRXUSDT': 'TRON',
        'LINKUSDT': 'Chainlink',
        'SHIBUSDT': 'Shiba Inu',
        'AVAXUSDT': 'Avalanche',
        'ATOMUSDT': 'Cosmos',
        'XMRUSDT': 'Monero',
        'UNIUSDT': 'Uniswap',
        'BCHUSDT': 'Bitcoin Cash',
        'ETCUSDT': 'Ethereum Classic',
        'APTUSDT': 'Aptos',
        'FILUSDT': 'Filecoin',
        'NEARUSDT': 'Near Protocol',
        'QNTUSDT': 'Quant',
        'VETUSDT': 'VeChain',
        'ICPUSDT': 'Internet Computer',
        'ALGOUSDT': 'Algorand',
        'EOSUSDT': 'EOS',
        'SANDUSDT': 'The Sandbox',
        'AAVEUSDT': 'Aave',
        'XTZUSDT': 'Tezos',
        'THETAUSDT': 'Theta Network',
        'EGLDUSDT': 'MultiversX',
        'GRTUSDT': 'The Graph',
        'CAKEUSDT': 'PancakeSwap',
        'XLMUSDT': 'Stellar',
        'FTMUSDT': 'Fantom',
        'RUNEUSDT': 'THORChain',
        'ZECUSDT': 'Zcash',
        'CHZUSDT': 'Chiliz',
        'ENJUSDT': 'Enjin Coin',
        'SNXUSDT': 'Synthetix',
        'CRVUSDT': 'Curve DAO',
        'COMPUSDT': 'Compound',
        'KSMUSDT': 'Kusama',
        'YFIUSDT': 'yearn.finance',
        '1INCHUSDT': '1inch',
        'BATUSDT': 'Basic Attention Token',
        'OMGUSDT': 'OMG Network',
        'DASHUSDT': 'Dash',
        'ZRXUSDT': '0x',
        'LRCUSDT': 'Loopring',
        'CVCUSDT': 'Civic',
        'STORJUSDT': 'Storj',
        'SUSHIUSDT': 'SushiSwap',
        'BALUSDT': 'Balancer',
        'BNTUSDT': 'Bancor',
        'RENUSDT': 'Ren',
        'SRMUSDT': 'Serum',
        'ANTUSDT': 'Aragon',
        'OCEANUSDT': 'Ocean Protocol',
        'FETUSDT': 'Fetch.ai',
        'CELRUSDT': 'Celer Network',
        'DENTUSDT': 'Dent',
        'HOTUSDT': 'Holo',
        'MTLUSDT': 'Metal',
        'STMXUSDT': 'StormX',
        'TWTUSDT': 'Trust Wallet Token',
        'CTSIUSDT': 'Cartesi',
        'AKROUSDT': 'Akropolis',
        'BANDUSDT': 'Band Protocol',
        'LPTUSDT': 'Livepeer',
        'MKRUSDT': 'Maker',
        'GALAUSDT': 'Gala',
        'FLUXUSDT': 'Flux',
        'COTIUSDT': 'COTI',
        'SKLUSDT': 'SKALE',
        'STPTUSDT': 'STP',
        'CTKUSDT': 'CertiK',
        'KAVAUSDT': 'Kava',
        'XVSUSDT': 'Venus',
        'SXPUSDT': 'Solar',
        'FORTHUSDT': 'Ampleforth Governance',
        'TOMOUSDT': 'TomoChain',
        'PERLUSDT': 'PERL.eco',
        'MDTUSDT': 'Measurable Data Token',
        'DGBUSDT': 'DigiByte',
        'NKNUSDT': 'NKN',
        'VTHOUSDT': 'VeThor Token',
        'PHAUSDT': 'Phala Network',
        'LITUSDT': 'Litentry',
        'SUNUSDT': 'SUN',
        'CVCUSDT': 'Civic',
        'BTSUSDT': 'BitShares',
        'ARPAUSDT': 'ARPA Chain',
        'DOCKUSDT': 'Dock',
        'TROYUSDT': 'TROY',
        'CTSIUSDT': 'Cartesi',
        'BUSDUSDT': 'Binance USD',
        'USDCUSDT': 'USD Coin',
        'USDTUSDT': 'Tether',
    }
    crypto_names = [f"{symbol_name_map.get(c['symbol'], c['symbol'])} ({c['symbol']})" for c in crypto_list]
    crypto_ids = [c['symbol'] for c in crypto_list]

    selected = st.selectbox('Select a cryptocurrency:', options=range(len(crypto_names)), format_func=lambda x: crypto_names[x])
    selected_id = crypto_ids[selected]

    if selected_id:
        st.subheader(f"{crypto_names[selected]} Price Data")
        df = get_crypto_history(selected_id)
        currentPrice = df['price'].iloc[-1] if not df.empty else 'N/A'
        st.write("Current Price (USD):", currentPrice)
        if not df.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['date'], y=df['price'], mode='lines', name='Price'))
            fig.update_layout(title='Historical Price (Last 30 Days)', xaxis_title='Date', yaxis_title='Price (USD)')
            st.plotly_chart(fig)
        else:
            st.write('No data available.')