import streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
import pydeck as pdk
import gc

st.set_page_config(page_title="Luxe Property | Sales Analytics", layout="wide")

hide_streamlit_style = """
            <style>
            [data-testid="stAppViewContainer"] { background-color: #000000; }
            [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="metric-container"] {
                background-color: #0A0A0A;
                border-radius: 8px;
                padding: 15px;
                border-left: 2px solid #B8860B;
                border-top: 1px solid #222222;
                border-bottom: 1px solid #222222;
                border-right: 1px solid #222222;
                box-shadow: 0 4px 6px rgba(0,0,0,0.5);
            }
            p, h1, h2, h3, h4, h5, h6, label { color: #FFFFFF !important; }
            .stSlider [role="slider"] {
                background-color: #B8860B !important; 
                border: 2px solid #E5C158 !important; 
                box-shadow: 0 0 10px rgba(184, 134, 11, 0.4) !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

@st.cache_dataport streamlit as st
import pandas as pd
import numpy as np
from streamlit_echarts import st_echarts, JsCode
import pydeck as pdk
import gc

st.set_page_config(page_title="Luxe Property | Sales Analytics", layout="wide")

hide_streamlit_style = """
            <style>
            [data-testid="stAppViewContainer"] { background-color: #000000; }
            [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div[data-testid="metric-container"] {
                background-color: #0A0A0A;
                border-radius: 8px;
                padding: 15px;
                border-left: 2px solid #B8860B;
                border-top: 1px solid #222222;
                border-bottom: 1px solid #222222;
                border-right: 1px solid #222222;
                box-shadow: 0 4px 6px rgba(0,0,0,0.5);
            }
            p, h1, h2, h3, h4, h5, h6, label { color: #FFFFFF !important; }
            .stSlider [role="slider"] {
                background-color: #B8860B !important; 
                border: 2px solid #E5C158 !important; 
                box-shadow: 0 0 10px rgba(184, 134, 11, 0.4) !important;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

@st.cache_data
