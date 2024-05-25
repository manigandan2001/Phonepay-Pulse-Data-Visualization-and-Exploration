Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly

Libraries used:
import json
import pandas as pd
import os
import mysql.connector
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests  
import streamlit as st  
from streamlit_lottie import st_lottie 

There are 4 .py files in this project
1 capstone2.py
2 1_🏠_Homepage.py
3 2_🇮🇳_GeoVisualization.py
4 3_📊_Insight.py

capstone2.py
* Data is cloned from the PhonePay Pulse github repository and saved in the local system.
* Data is extracted and stored as a data frame.
* Data pre processing is done.
* Creating Sql tables.
* Storing the data in the respective sql table.

Since my streamlit application is a multipage application, it has 3 different .py files.
1_🏠_Homepage.py
* Animation is displayed using streamlit_lottie
* It has the details of the project, tools used.

2_🇮🇳_GeoVisualization.py
* Animation is imported using streamlit_lottie
* An option of choosing the year from 2018 to 2024 is given to the user using streamlit widget.
* An option of choosing the quater from 1 to 4 is given to the user using streamlit widget.
* A An option of choosing between transaction data and user data is given to the user using streamlit widget.
* Based on the input given by the user, an live geo visualization dashboard that displays
information and insights from the Phonepe pulse Github repository in an interactive
and visually appealing manner is displayed using plotly inbuilt function.

3_📊_Insight.py
* Animation is imported using streamlit_lottie
* A drop down option of 11 various insights are provided to the user using streamlit widget.
Region Wise Transaction Data
Top 10 Districts Overall Data
Top 10 States Overall Data
Most Popular Transaction Type Data
Transaction And User Data Of A Particular State
Seasonal Effect
High Value Transaction Data
App Usage Intensity Data
Top 5 Pincodes That Has Done High Transaction In Tamil Nadu
Distribution Of Users By Brand
* Based on the choosen topic, a chart is displayed on the dashboard, providing the user with various insights about the Phonepay Pulse data.
