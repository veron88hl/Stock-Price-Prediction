from curses import window
from distutils.log import info
import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime

import talib 
import ta
import requests
yf.pdr_override()

def show_explore_page():
    PlaceHolder ='empty'
    # App title
    st.markdown('''
    # Company Data
    For query companies!''')

    # Sidebar
    st.sidebar.subheader('Query Parameters')
    start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
    end_date = st.sidebar.date_input("End date", datetime.date(2021, 1, 31))

    # Retrieving tickers data
    tickerSymbol = st.text_input('Please enter your company ticker:') 

    st.write('---')

    tickerData = yf.Ticker(tickerSymbol) # Get ticker data
    tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

    # Ticker information
    string_logo = '<img src=%s>' % tickerData.info['logo_url']
    st.markdown(string_logo, unsafe_allow_html=True)

    # Ticker data
    st.header('**Technical Data**')
    st.write(tickerDf)


    ####

    # Read data 
    #data = yf.download(tickerSymbol,start,end)

    company_name = tickerSymbol.upper()
    data = web.DataReader(tickerSymbol, data_source='yahoo', start=start_date, end=end_date)

    #Close Price
    st.header(f"Close Price\n {company_name}")
    st.line_chart(data['Close'])

    # Adjusted Close Price
    st.header(f"Adjusted Close Price\n {company_name}")
    st.line_chart(data['Adj Close'])

    # ## SMA and EMA
    #Simple Moving Average
    data['SMA'] = talib.SMA(data['Adj Close'], timeperiod = 20)

    # Exponential Moving Average
    data['EMA'] = talib.EMA(data['Adj Close'], timeperiod = 20)

    # Plot
    st.header(f"Simple Moving Average vs. Exponential Moving Average\n {company_name}")
    st.line_chart(data[['Adj Close','SMA','EMA']])

    # Bollinger Bands
    data['upper_band'], data['middle_band'], data['lower_band'] = talib.BBANDS(data['Adj Close'], timeperiod =20)

    # Plot
    st.header(f"Bollinger Bands\n {company_name}")
    st.line_chart(data[['Adj Close','upper_band','middle_band','lower_band']])

    # ## MACD (Moving Average Convergence Divergence)
    # MACD
    data['macd'], data['macdsignal'], data['macdhist'] = talib.MACD(data['Adj Close'], fastperiod=12, slowperiod=26, signalperiod=9)

    # Plot
    st.header(f"Moving Average Convergence Divergence\n {company_name}")
    st.line_chart(data[['macd','macdsignal']])

    ## CCI (Commodity Channel Index)
    # CCI
    cci = ta.trend.cci(data['High'], data['Low'], data['Close'], window=31, constant=0.015)

    # Plot
    st.header(f"Commodity Channel Index\n {company_name}")
    st.line_chart(cci)

    # ## RSI (Relative Strength Index)
    # RSI
    data['RSI'] = talib.RSI(data['Adj Close'], timeperiod=14)

    # Plot
    st.header(f"Relative Strength Index\n {company_name}")
    st.line_chart(data['RSI'])

    # ## OBV (On Balance Volume)
    # OBV
    data['OBV'] = talib.OBV(data['Adj Close'], data['Volume'])/10**6

    # Plot
    st.header(f"On Balance Volume\n {company_name}")
    st.line_chart(data['OBV'])

    if st.button('Fundamental Data'):
        st.header('**Fundamental Data**')
        tickerinfo = yf.Ticker(tickerSymbol)
        st.markdown('''Financials''')
        st.write(tickerinfo.quarterly_financials)
        st.write('---')
        st.markdown('''Balance Sheet''')
        st.write(tickerinfo.quarterly_balance_sheet)
        st.write('---')
        st.markdown('''Cashflow''')
        st.write(tickerinfo.quarterly_cashflow)
        st.write('---')
        st.markdown('''Recommendations by Analysts (via yfinance)''')
        st.write(tickerinfo.recommendations)
        st.write('---')
    