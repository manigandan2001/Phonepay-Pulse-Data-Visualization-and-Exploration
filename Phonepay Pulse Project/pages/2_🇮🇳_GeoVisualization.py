import json
import pandas as pd
import os
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

import requests  # pip install requests
import streamlit as st  # pip install streamlit
from streamlit_lottie import st_lottie  # pip install streamlit-lottie

# Database connection details
user = 'root'
password = 'Digi08@Life'
host = 'localhost'
database = 'capstone2_phonepay'

# Connect to the database
conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = conn.cursor()


st.set_page_config(
    page_title="Homepage",
    page_icon="🏠",
)

heading_text = "<span style='color:#FF9933'>Geo</span> <span style='color:#FFFFFF'>Visual</span><span style='color:#008000'>ization</span>"

# Display the heading using Markdown
st.markdown(f"<h1>{heading_text}</h1>", unsafe_allow_html=True)
st.sidebar.success("Select a page from above")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/18de2a6b-c0d2-4cd5-9622-56cee4718734/COh7Ndz0ec.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    height=None,
    width=None,
    key= "WELCOME",)

Year = st.slider("Enter the year of data you want to view", min_value=2018, max_value=2024)
Quater = st.slider("Enter the quater of data you want to view", min_value=1, max_value=4)
Type = st.selectbox("Enter the type of data you want to view", ("Transaction Data", "User Data"))
if st.button("Submit"):
    
    if Type == "Transaction Data":
            st.markdown("## <span style='color: yellow;'>Aggregated Transaction Data On India Map</span>", unsafe_allow_html=True)
            sql_query = f"""
                            SELECT State, Year, Quater, 
                            SUM(Transaction_count) as Transaction_count, 
                            SUM(Transaction_amount) as Transaction_amount, 
                            SUM(Transaction_count) + SUM(Transaction_amount) as aggregated_transaction_data
                            FROM Aggregated_Transaction
                            WHERE Year = '{Year}' AND Quater = '{Quater}'
                            GROUP BY State, Year, Quater
                            """
            color_column = 'aggregated_transaction_data'
            hover_data = {'Transaction_amount': True, 'Transaction_count': True, 'aggregated_transaction_data': False}
            color_scale = 'Reds'
            title_text = f'Transaction Data for Year {Year}, Quarter {Quater}'
            color_bar_title = 'Aggregated Transaction Data'
    elif Type == "User Data":
        st.markdown("## <span style='color: yellow;'>Aggregated User Data On India Map</span>", unsafe_allow_html=True)
        sql_query = f"""
                        SELECT State, Year, Quater, 
                        SUM(No_of_users) as registered_users, 
                        SUM(Total_app_open) as Total_app_open, 
                        SUM(No_of_users) + SUM(Total_app_open) as aggregated_user_data
                        FROM map_user
                        WHERE Year = '{Year}' AND Quater = '{Quater}'
                        GROUP BY State, Year, Quater
                        """
        color_column = 'aggregated_user_data'
        hover_data = {'registered_users': True, 'Total_app_open': True, 'aggregated_user_data': False}
        color_scale = 'Blues'
        title_text = f'User Data for Year {Year}, Quarter {Quater}'
        color_bar_title = 'Aggregated User Data'

    # Read the SQL query into a DataFrame
    df = pd.read_sql(sql_query, conn)

    # Create the choropleth map
    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color=color_column,
        hover_data=hover_data,
        color_continuous_scale=color_scale
    )

    # Update the layout to include the title with year and quarter
    fig.update_layout(
        title_text=title_text,
        coloraxis_colorbar=dict(
            title=color_bar_title
        )
    )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True)