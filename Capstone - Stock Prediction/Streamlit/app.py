#https://github.com/dataprofessor/code/blob/master/streamlit/part10/sp500-app.py

from distutils.log import error
from symtable import Symbol
import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

from predict_page import show_predict_page
from explore_page import show_explore_page
from recommend_page import recommendation_page


page = st.sidebar.selectbox("What would you like to do today?", ("Predict", "Explore"))

if page == "Predict":
    show_predict_page()

else:
    show_explore_page()