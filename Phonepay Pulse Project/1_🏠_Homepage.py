import json

import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

st.markdown(
    """
    <h1 style='text-align: center;'>
        <span style='color: #800080;'>Phonepe Pulse</span> Data Visualization and Exploration
    </h1>
    """, 
    unsafe_allow_html=True
)
st.sidebar.success("Select a page from above")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/28ab51fe-7e2f-4996-a8cf-17c089c8e603/mFId1gNFg3.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    height=None,
    width=None,
    key= "WELCOME",
)
st.markdown(
    """
    <h1 style='text-align: center; color: white;'>
        Welcome to the Homepage of 
        <span style='color: #800080;'>Phonepe Pulse</span> 
        <span style='color: lightblue;'>Data Visualization</span> 
        <span style='color: white;'>and</span> 
        <span style='color: #6c8ebf;'>Exploration</span>
    </h1>
    """, 
    unsafe_allow_html=True
)
st.write("This project extracts data from the phonepe pulse github repository, that contains a large amount of data related to various metrics and statistics. The obtained data is processed and used to get insights and information that can be visualized in a user-friendly manner.")
st.markdown("<span style='color: cyan;'>Result:</span>", unsafe_allow_html=True)
st.write("""The result of this project will be a live geo visualization dashboard that displays
information and insights from the Phonepe pulse Github repository in an interactive
and visually appealing manner. The Insight page will have at least 10 different
dropdown options for users to select different facts and figures to display. The data
will be stored in a MySQL database for efficient retrieval and the dashboard will be
dynamically updated to reflect the latest data.
Users will be able to access the dashboard from a web browser and easily navigate
the different visualizations and facts and figures displayed. The dashboard will
provide valuable insights and information about the data in the Phonepe pulse
Github repository, making it a valuable tool for data analysis and decision-making.
Overall, the result of this project will be a comprehensive and user-friendly solution
for extracting, transforming, and visualizing data from the Phonepe pulse Github
repository.""")
st.markdown("<span style='color: cyan;'>Domain:</span> <span style='color: white;'>Fintech</span>", unsafe_allow_html=True)
st.markdown("<span style='color: cyan;'>Technologies used:</span> Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly", unsafe_allow_html=True)

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/848871b3-eeda-4854-9bc8-7616e2ffe678/f86GBVkM7M.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low")