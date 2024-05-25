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

st.markdown("## <span style='color: violet;'>Data Visualization and Insights</span>", unsafe_allow_html=True)
st.sidebar.success("Select a page from above")

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_hello = load_lottieurl("https://lottie.host/3e050f40-9880-4493-b1c8-d8485803fa5f/oqQvIN3BuD.json")

st_lottie(
    lottie_hello,
    speed=1,
    reverse=False,
    loop=True,
    quality="low", # medium ; high
    height=None,
    width=None,
    key= "WELCOME",)

options = ["Region Wise Transaction Data","Top 10 Districts Overall Data", "Top 10 States Overall Data",
           "Most Popular Transaction Type Data","Transaction And User Data Of A Particular State","Seasonal Effect",
           "High Value Transaction Data", "App Usage Intensity Data","Top 5 Pincodes That Has Done High Transaction In Tamil Nadu",
           "Distribution Of Users By Brand"]

# Add a selectbox to the sidebar
selected_option = st.sidebar.selectbox('Select an option:', options)

if selected_option == "Region Wise Transaction Data":
    metrics_options = ["Transaction Amount", "Transaction Count"]
    selected_metric = st.selectbox('Select a metric:', metrics_options)

    regions = {
        "East India": ["Bihar", "Jharkhand", "Odisha", "West Bengal"],
        "West India": ["Goa", "Gujarat", "Maharashtra", "Rajasthan"],
        "North India": ["Chandigarh", "Delhi", "Haryana", "Himachal Pradesh", "Jammu & Kashmir", "Ladakh", "Punjab", "Uttar Pradesh", "Uttarakhand"],
        "South India": ["Andhra Pradesh", "Karnataka", "Kerala", "Tamil Nadu", "Telangana", "Puducherry"],
        "Central India": ["Chhattisgarh", "Madhya Pradesh"],
        "North-East India": ["Arunachal Pradesh", "Assam", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Sikkim", "Tripura"]
    }

    state_to_region = {state: region for region, states in regions.items() for state in states}

    if selected_metric == "Transaction Amount":
        # Fetch data from the database
        df = pd.read_sql("SELECT State, Year, SUM(Transaction_amount) as Total_Transaction_Amount FROM Aggregated_Transaction GROUP BY State, Year", conn)

        # Map states to regions
        df['Region'] = df['State'].map(state_to_region)

        # Filter out data for the years 2018 and 2024
        df_filtered = df[(df['Year'] != 2018) & (df['Year'] != 2024)]

        # Group by region and year, then sum transaction amounts
        region_yearly_transactions = df_filtered.groupby(['Region', 'Year'])['Total_Transaction_Amount'].sum().reset_index()

        # Plot the data
        fig = px.line(region_yearly_transactions, x='Year', y='Total_Transaction_Amount', color='Region', markers=True,
                      title='Total Transaction Amount by Region (Excluding 2018 and 2024)',
                      labels={'Total_Transaction_Amount': 'Total Transaction Amount', 'Year': 'Year'},
                      template='plotly_dark')

        # Update layout for better visualization
        fig.update_layout(autosize=False, width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "Transaction Count":
        # Fetch data from the database
        df = pd.read_sql("SELECT State, Year, SUM(Transaction_count) as Total_Transaction_Count FROM Aggregated_Transaction GROUP BY State, Year", conn)

        # Map states to regions
        df['Region'] = df['State'].map(state_to_region)

        # Filter out data for the years 2018 and 2024
        df_filtered = df[(df['Year'] != 2018) & (df['Year'] != 2024)]

        # Group by region and year, then sum transaction counts
        region_yearly_count = df_filtered.groupby(['Region', 'Year'])['Total_Transaction_Count'].sum().reset_index()

        # Plot the data
        fig = px.line(region_yearly_count, x='Year', y='Total_Transaction_Count', color='Region', markers=True,
                      title='Total Transaction Count by Region (Excluding 2018 and 2024)',
                      labels={'Total_Transaction_Count': 'Total Transaction Count', 'Year': 'Year'},
                      template='plotly_dark')

        # Update layout for better visualization
        fig.update_layout(autosize=False, width=1000, height=600)
        st.plotly_chart(fig, use_container_width=True) 


elif selected_option == "Top 10 Districts Overall Data":
    metrics_options = ["Transaction Amount", "Transaction Count", "App Open", "Registered Users"]
    selected_metric = st.selectbox('Select a metric:', metrics_options)

    if selected_metric == "Transaction Amount":
        query = """
            SELECT District_name, SUM(Total_amount) as Total_Transaction_Amount
            FROM map_transaction
            GROUP BY District_name
            ORDER BY Total_Transaction_Amount DESC
            LIMIT 10;
        """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='District_name',
            y='Total_Transaction_Amount',
            title='Top 10 Districts with Highest Transaction Amount',
            labels={'District_name': 'District Name', 'Total_Transaction_Amount': 'Total Transaction Amount'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='District Name',
            yaxis_title='Total Transaction Amount',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "Transaction Count":
        query = """
            SELECT District_name, SUM(No_of_transaction) as Total_Transaction_Count
            FROM map_transaction
            GROUP BY District_name
            ORDER BY Total_Transaction_Count DESC
            LIMIT 10;
        """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='District_name',
            y='Total_Transaction_Count',
            title='Top 10 Districts with Highest Transaction Count',
            labels={'District_name': 'District Name', 'Total_Transaction_Count': 'Total Transaction Count'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='District Name',
            yaxis_title='Total Transaction Count',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "App Open":
        query = """
            SELECT District_name, SUM(Total_app_open) as Total_App_Open
            FROM map_user
            GROUP BY District_name
            ORDER BY Total_App_Open DESC
            LIMIT 10;
        """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='District_name',
            y='Total_App_Open',
            title='Top 10 Districts with Highest App Open',
            labels={'District_name': 'District Name', 'Total_App_Open': 'Total App Open'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='District Name',
            yaxis_title='Total App Open',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "Registered Users":
        query = """
            SELECT District_name, SUM(No_of_users) as No_of_users
            FROM map_user
            GROUP BY District_name
            ORDER BY No_of_users DESC
            LIMIT 10;
        """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='District_name',
            y='No_of_users',
            title='Top 10 Districts with Highest Number of Users',
            labels={'District_name': 'District Name', 'No_of_users': 'No of users'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='District Name',
            yaxis_title='No of users',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_option == "Top 10 States Overall Data":
    metrics_options = ["Transaction Amount", "Transaction Count", "Registered Users"]
    selected_metric = st.selectbox('Select a metric:', metrics_options)

    if selected_metric == "Transaction Amount":
        query = """
                SELECT State, SUM(Transaction_amount) as Total_Transaction_Amount
                FROM Aggregated_Transaction
                GROUP BY State
                ORDER BY Total_Transaction_Amount DESC
                LIMIT 10;
            """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='State',
            y='Total_Transaction_Amount',
            title='Top 10 States with Highest Transaction Amount',
            labels={'State': 'State', 'Total_Transaction_Amount': 'Total Transaction Amount'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='State',
            yaxis_title='Total Transaction Amount',
            autosize=False,
            width=800,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "Transaction Count":
        query = """
                SELECT State, SUM(Transaction_count) as Total_Transaction_Count
                FROM Aggregated_Transaction
                GROUP BY State
                ORDER BY Total_Transaction_Count DESC
                LIMIT 10;
            """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='State',
            y='Total_Transaction_Count',
            title='Top 10 States with Highest Transaction Count',
            labels={'State': 'State', 'Total_Transaction_Count': 'Total Transaction Count'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='State',
            yaxis_title='Total Transaction Count',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

    elif selected_metric == "Registered Users":
        query = """
                    SELECT State, SUM(Total_users) as Total_Registered_Users
                    FROM Aggregated_user
                    GROUP BY State
                    ORDER BY Total_Registered_Users DESC
                    LIMIT 10;
                """
        # Fetch data
        df = pd.read_sql(query, conn)
        # Create a bar plot
        fig = px.bar(
            df,
            x='State',
            y='Total_Registered_Users',
            title='Top 10 States with Highest Registered Users',
            labels={'State': 'State', 'Total_Registered_Users': 'Total Registered Users'},
            template='plotly_dark'
        )
        # Update layout for better visualization
        fig.update_layout(
            xaxis_title='State',
            yaxis_title='Total Registered Users',
            autosize=False,
            width=800,
            height=600
        )
        st.plotly_chart(fig, use_container_width=True)

elif selected_option == "Most Popular Transaction Type Data":
    query = """
            select Transaction_type, sum(Transaction_count) as Total_Transantion_Count 
            from Aggregated_Transaction
            group by Transaction_type;
            """       
    # Fetch data
    df = pd.read_sql(query, conn)
    fig = px.pie(
            df,
            names='Transaction_type',
            values='Total_Transantion_Count',
            title='Most Popular Transaction Types',
            template='plotly_dark'
        )
        # Update layout for better visualization
    fig.update_layout(
            autosize=False,
            width=800,
            height=600
        )
    st.plotly_chart(fig, use_container_width=True)

elif selected_option == "Transaction And User Data Of A Particular State":
    Year = st.slider("Enter the year of data you want to view", min_value=2018, max_value=2024)
    Quater = st.slider("Enter the quater of data you want to view", min_value=1, max_value=4)
    State = st.selectbox("Enter the state name of data you want to view", ('Andaman & Nicobar ', 'Tamil Nadu', 'Lakshadweep', 'Telangana',
                                                                            'Manipur', 'Haryana', 'Gujarat', 'Sikkim', 'Delhi', 'West Bengal',
                                                                            'Uttar Pradesh', 'Goa', 'Punjab', 'Arunachal Pradesh', 'Karnataka',
                                                                            'Jammu & Kashmir', 'Maharashtra', 'Odisha', 'Madhya Pradesh',
                                                                            'Rajasthan', 'Andhra Pradesh', 'Chandigarh', 'Kerala',
                                                                            'Chhattisgarh', 'Tripura', 'Mizoram', 'Himachal Pradesh',
                                                                            'Dadra and Nagar Haveli and Daman and Diu', 'Ladakh', 'Assam',
                                                                            'Meghalaya', 'Uttarakhand', 'Puducherry', 'Bihar', 'Jharkhand',
                                                                            'Nagaland'))
    sql_query_transaction = f"""
                                SELECT District_name, Total_amount as Total_Transaction_Amount, No_of_Transaction as Total_Transaction_Count
                                FROM map_transaction
                                WHERE Year = '{Year}' AND Quater = '{Quater}' AND State = '{State}'
                                ORDER BY District_name DESC;
                            """
    sql_query_user = f"""
        SELECT District_name, No_of_users as Total_Registered_User, Total_app_open as Total_App_Open
        FROM map_user
        WHERE Year = '{Year}' AND Quater = '{Quater}' AND State = '{State}'
        ORDER BY District_name DESC;"""
    transaction_df = pd.read_sql(sql_query_transaction, conn)
    user_df = pd.read_sql(sql_query_user, conn)

    combined_df = pd.merge(transaction_df, user_df, on='District_name')

    # Create subplots for the treemaps
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Transaction Amount", "Transaction Count", "Total Registered Users", "Total App Opens"),
        specs=[[{"type": "treemap"}, {"type": "treemap"}], [{"type": "treemap"}, {"type": "treemap"}]]
    )
    # Add treemap for Transaction Amount
    fig.add_trace(
        go.Treemap(
            labels=combined_df['District_name'],
            parents=[""] * len(combined_df),  # Each district is a top-level node
            values=combined_df['Total_Transaction_Amount'],
            name="Transaction Amount"
        ),
        row=1, col=1
    )
    # Add treemap for Transaction Count
    fig.add_trace(
        go.Treemap(
            labels=combined_df['District_name'],
            parents=[""] * len(combined_df),  # Each district is a top-level node
            values=combined_df['Total_Transaction_Count'],
            name="Transaction Count"
        ),
        row=1, col=2
    )

    # Add treemap for Total Registered Users
    fig.add_trace(
        go.Treemap(
            labels=combined_df['District_name'],
            parents=[""] * len(combined_df),  # Each district is a top-level node
            values=combined_df['Total_Registered_User'],
            name="Total Registered Users"
        ),
        row=2, col=1
    )

    # Add treemap for Total App Opens
    fig.add_trace(
        go.Treemap(
            labels=combined_df['District_name'],
            parents=[""] * len(combined_df),  # Each district is a top-level node
            values=combined_df['Total_App_Open'],
            name="Total App Opens"
        ),
        row=2, col=2
    )

    fig.update_layout(
        title_text=f'District-wise Data for {State}, Year {Year}, Quarter {Quater}',
        autosize=False,
        width=1000,
        height=800
    )
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "Seasonal Effect":
    sql_query ="""select Quater, sum(Transaction_count) as Total_Transaction_Count
                from Aggregated_Transaction
                group by Quater
                order by Quater;"""

    df = pd.read_sql(sql_query, conn)
    # Create a line plot using Plotly
    fig = px.line(df, x='Quater', y='Total_Transaction_Count', title='Total Transaction Count by Quarter',
                labels={'Quater': 'Quarter', 'Total_Transaction_Count': 'Total Transaction Count'})
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "High Value Transaction Data":
    query = """SELECT District_name, State, SUM(Total_amount) / SUM(No_of_transaction) AS High_Value_Transaction
                FROM map_transaction
                GROUP BY District_name, State
                ORDER BY High_Value_Transaction DESC
                LIMIT 50;"""
    df = pd.read_sql(query, conn)
    # Create a bar plot using Plotly Express
    fig = px.bar(df, x='District_name', y='High_Value_Transaction', color='State', 
                title='Average High Value Transaction by District and State',
                labels={'High_Value_Transaction': 'Average High Value Transaction'},
                template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "App Usage Intensity Data":
    #app usage intensity
    query = """SELECT District_name, State, SUM(Total_app_open) / SUM(No_of_users) AS App_Usage_Intensity
    FROM map_user
    GROUP BY District_name, State
    ORDER BY App_Usage_Intensity DESC
    LIMIT 50;"""
    df = pd.read_sql(query, conn)
    # Assuming df is your DataFrame containing the data
    fig = px.bar(df, x='District_name', y='App_Usage_Intensity', color='State', 
                title='Average App Usage Intensity by District and State',
                labels={'App_Usage_Intensity': 'Average App Usage Intensity'},
                template='plotly_dark')
    # Rotate x-axis labels by 45 degrees for better readability
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "Top 5 Pincodes That Has Done High Transaction In Tamil Nadu":
    query = """
                SELECT Pincode, Sum(Total_pincode_transactions_amount) as Total_Transaction_Amount 
                FROM top_transaction_pincode
                WHERE State = 'Tamil Nadu'
                GROUP BY Pincode
                ORDER BY Total_Transaction_Amount Desc
                LIMIT 5;
                """
    df = pd.read_sql(query, conn)        
    # Convert Pincode to string to treat it as categorical data
    df['Pincode'] = df['Pincode'].astype(str)
    # Create a bar chart using Plotly Express
    fig = px.bar(df, x='Pincode', y='Total_Transaction_Amount', 
                title='Top 10 Pin Codes in Tamil Nadu by Total Transaction Amount',
                labels={'Pincode': 'Pincode', 'Total_Transaction_Amount': 'Total Transaction Amount'},
                template='plotly_dark',
                color='Pincode')  # Assign different colors to different pin codes
    st.plotly_chart(fig, use_container_width=True)
elif selected_option == "Distribution Of Users By Brand":
    query = """
                SELECT Brand_name, SUM(No_of_users) AS Total_Users
                FROM Aggregated_user
                GROUP BY Brand_name;
            """
    # Execute the query and load the data into a DataFrame
    df = pd.read_sql(query, conn)
    # Create a pie chart using Plotly Express
    fig = px.pie(df, names='Brand_name', values='Total_Users', 
                title='Distribution of Users by Brand',
                template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)