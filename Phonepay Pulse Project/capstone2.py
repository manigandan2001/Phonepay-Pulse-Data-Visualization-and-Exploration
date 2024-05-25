import json
import pandas as pd
import os
import mysql.connector

# Database connection details
user = 'root'
password = 'Digi08@Life'
host = 'localhost'
database = 'capstone2_phonepay'

# Connect to the database
conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
cursor = conn.cursor()

path="/Users/sanjay/Documents/capstone 2 data/data/aggregated/transaction/country/india/state/"
all_state_names = os.listdir(path)

empty_dict ={'State':[], 'Year':[],'Quater':[],'Transaction_type':[], 'Transaction_count':[], 'Transaction_amount':[]}
for state in all_state_names:
    path_of_year = path+state+'/'
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        for i in D['data']['transactionData']:
          Name = i['name']
          count = i['paymentInstruments'][0]['count']
          amount= i['paymentInstruments'][0]['amount']
          empty_dict['Transaction_type'].append(Name)
          empty_dict['Transaction_count'].append(count)
          empty_dict['Transaction_amount'].append(amount)
          empty_dict['State'].append(state)
          empty_dict['Year'].append(year)
          empty_dict['Quater'].append(int(quater.strip('.json')))
#creating a dataframe
Aggregated_Transaction = pd.DataFrame(empty_dict)

Aggregated_Transaction = Aggregated_Transaction.drop_duplicates()
Aggregated_Transaction['State'] = Aggregated_Transaction['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

empty_dict = {'State':[], 'Year':[],'Quater':[],'Brand_name':[], 'No_of_users':[], 'Percent_of_share':[], 'Total_users': []}
path="/Users/sanjay/Documents/capstone 2 data/data/aggregated/user/country/india/state/"
for state in all_state_names:
    path_of_year = path+state+"/"
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        total_user_count = D['data']['aggregated']['registeredUsers']
        if D['data'].get('usersByDevice') is not None:
          for i in D['data'].get('usersByDevice',[]):
            name_of_brand = i.get('brand', '')
            user_count = i['count']
            percent = i['percentage']
            empty_dict['Total_users'].append(int(total_user_count))
            empty_dict['Brand_name'].append(name_of_brand)
            empty_dict['No_of_users'].append(user_count)
            empty_dict['Percent_of_share'].append(percent)
            empty_dict['State'].append(state)
            empty_dict['Year'].append(year)
            empty_dict['Quater'].append(int(quater.strip('.json')))
#creating a dataframe
Aggregated_user = pd.DataFrame(empty_dict)

Aggregated_user = Aggregated_user.drop_duplicates()
Aggregated_user['State'] = Aggregated_user['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

path = "/Users/sanjay/Documents/capstone 2 data/data/map/transaction/hover/country/india/state/"
empty_dict = {'State':[], 'Year':[],'Quater':[], 'No_of_transaction':[], 'Total_amount':[], 'District_name':[]}
for state in all_state_names:
    path_of_year = path+state+"/"
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        for i in D['data']['hoverDataList']:
          district = i['name']
          total_transaction = i['metric'][0]['count']
          amount = i['metric'][0]['amount']
          empty_dict['District_name'].append(district)
          empty_dict['No_of_transaction'].append(total_transaction)
          empty_dict['Total_amount'].append(amount)
          empty_dict['State'].append(state)
          empty_dict['Year'].append(year)
          empty_dict['Quater'].append(int(quater.strip('.json')))
#creating a dataframe
map_transaction = pd.DataFrame(empty_dict)

map_transaction = map_transaction.drop_duplicates()
map_transaction['State'] = map_transaction['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

path =  "/Users/sanjay/Documents/capstone 2 data/data/map/user/hover/country/india/state/"
empty_dict = {'State':[], 'Year':[],'Quater':[], 'No_of_users':[], 'Total_app_open':[], 'District_name':[]}
for state in all_state_names:
    path_of_year = path+state+"/"
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        for district, district_data in D['data']['hoverData'].items():
          name_of_district = district
          total_users = district_data['registeredUsers']
          no_of_appopens = district_data['appOpens']
          empty_dict['No_of_users'].append(total_users)
          empty_dict['Total_app_open'].append(no_of_appopens)
          empty_dict['District_name'].append(name_of_district)
          empty_dict['State'].append(state)
          empty_dict['Year'].append(year)
          empty_dict['Quater'].append(int(quater.strip('.json')))
#creating a dataframe
map_user = pd.DataFrame(empty_dict)

map_user = map_user.drop_duplicates()
map_user['State'] = map_user['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

path = "/Users/sanjay/Documents/capstone 2 data/data/top/transaction/country/india/state/"
empty_dict = {'State':[], 'Year':[],'Quater':[], 'Total_district_transactions_no':[], 'Total_district_transactions_amount':[], 'District_name':[]}
empty_dict1 = {'State':[], 'Year':[],'Quater':[], 'Pincode':[], 'Total_pincode_transactions_no':[], 'Total_pincode_transactions_amount':[]}

for state in all_state_names:
    path_of_year = path+state+"/"
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        for i in D['data']['districts']:
          district = i['entityName']
          district_count = i['metric']['count']
          district_amount = i['metric']['amount']
          empty_dict['District_name'].append(district)
          empty_dict['Total_district_transactions_amount'].append(district_amount)
          empty_dict['Total_district_transactions_no'].append(district_count)
          empty_dict['State'].append(state)
          empty_dict['Year'].append(year)
          empty_dict['Quater'].append(int(quater.strip('.json')))
        for i in D['data']['pincodes']:
          pincode = i['entityName']
          pincode_count = i['metric']['count']
          pincode_amount = i['metric']['amount']
          empty_dict1['Pincode'].append(pincode)
          empty_dict1['Total_pincode_transactions_amount'].append(pincode_amount)
          empty_dict1['Total_pincode_transactions_no'].append(pincode_count)
          empty_dict1['State'].append(state)
          empty_dict1['Year'].append(year)
          empty_dict1['Quater'].append(int(quater.strip('.json')))
#creating a dataframe
top_transaction_district = pd.DataFrame(empty_dict)
top_transaction_pincode = pd.DataFrame(empty_dict1)

top_transaction_district = top_transaction_district.drop_duplicates()
top_transaction_district['State'] = top_transaction_district['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

top_transaction_pincode = top_transaction_pincode.drop_duplicates()
top_transaction_pincode['State'] = top_transaction_pincode['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

path = "/Users/sanjay/Documents/capstone 2 data/data/top/user/country/india/state/"
empty_dict = {'State':[], 'Year':[],'Quater':[], 'Total_district_registered_users':[], 'District_name':[]}
empty_dict1 = {'State':[], 'Year':[],'Quater':[], 'Total_pincode_registered_users':[], 'pincode':[]}
for state in all_state_names:
    path_of_year = path+state+"/"
    list_of_years = os.listdir(path_of_year)
    for year in list_of_years:
      path_of_quater = path_of_year+year+"/"
      list_of_quater = os.listdir(path_of_quater)
      for quater in list_of_quater:
        path_of_json = path_of_quater+quater
        Data = open(path_of_json,'r')
        D= json.load(Data)
        for i in D['data']['districts']:
          district = i['name']
          total_district_users = i['registeredUsers']
          empty_dict['Total_district_registered_users'].append(total_district_users)
          empty_dict['District_name'].append(district)
          empty_dict['State'].append(state)
          empty_dict['Year'].append(year)
          empty_dict['Quater'].append(int(quater.strip('.json')))
        for i in D['data']['pincodes']:
          pincode = i['name']
          total_pincode_users = i['registeredUsers']
          empty_dict1['Total_pincode_registered_users'].append(total_pincode_users)
          empty_dict1['pincode'].append(pincode)
          empty_dict1['State'].append(state)
          empty_dict1['Year'].append(year)
          empty_dict1['Quater'].append(int(quater.strip('.json')))

top_user_district = pd.DataFrame(empty_dict)
top_user_pincode = pd.DataFrame(empty_dict1)

top_user_district = top_user_district.drop_duplicates()
top_user_district['State'] = top_user_district['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

top_user_pincode = top_user_pincode.drop_duplicates()
top_user_pincode['State'] = top_user_pincode['State'].apply(lambda x: x.title().replace("Islands","").replace("-"," ").replace("Dadra & Nagar Haveli & Daman & Diu","Dadra and Nagar Haveli and Daman and Diu"))

# Create table if it doesn't exist
create_table_query = "CREATE TABLE IF NOT EXISTS Aggregated_Transaction (State VARCHAR(255),Year INT,Quater INT,Transaction_type VARCHAR(255),Transaction_count INT,Transaction_amount FLOAT)"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS Aggregated_user (State VARCHAR(255),Year INT,Quater INT,Brand_name VARCHAR(100),No_of_users INT,Percent_of_share FLOAT,Total_users INT)"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS map_transaction (State VARCHAR(255),Year INT,Quater INT,No_of_transaction INT,Total_amount FLOAT,District_name VARCHAR(100))"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS map_user (State VARCHAR(255),Year INT,Quater INT,No_of_users INT,Total_app_open INT,District_name VARCHAR(100))"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS top_transaction_district (State VARCHAR(255),Year INT,Quater INT,Total_district_transactions_no INT,Total_district_transactions_amount FLOAT,District_name VARCHAR(100))"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS top_transaction_pincode (State VARCHAR(255),Year INT,Quater INT,Pincode INT,Total_pincode_transactions_no INT,Total_pincode_transactions_amount FLOAT)"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS top_user_district (State VARCHAR(255),Year INT,Quater INT,Total_district_registered_users INT,District_name VARCHAR(100))"
cursor.execute(create_table_query)

create_table_query = "CREATE TABLE IF NOT EXISTS top_user_pincode (State VARCHAR(255),Year INT,Quater INT,Total_pincode_registered_users INT,pincode INT)"
cursor.execute(create_table_query)

conn.commit()

for idx, row in Aggregated_Transaction.iterrows():
    sql_query = "INSERT INTO Aggregated_Transaction (State, Year, Quater, Transaction_type, Transaction_count, Transaction_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['Transaction_type'], row['Transaction_count'], row['Transaction_amount'])
    cursor.execute(sql_query, values)
    
for idx, row in Aggregated_user.iterrows():
    sql_query = "INSERT INTO Aggregated_user (State, Year, Quater,Brand_name, No_of_users, Percent_of_share, Total_users) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'],row['Brand_name'], row['No_of_users'], row['Percent_of_share'], row['Total_users'])
    cursor.execute(sql_query, values)

for idx, row in map_transaction.iterrows():
    sql_query = "INSERT INTO map_transaction (State, Year, Quater, No_of_transaction, Total_amount, District_name) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['No_of_transaction'], row['Total_amount'], row['District_name'])
    cursor.execute(sql_query, values)

for idx, row in map_user.iterrows():
    sql_query = "INSERT INTO map_user (State, Year, Quater, No_of_users, Total_app_open, District_name) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['No_of_users'], row['Total_app_open'], row['District_name'])
    cursor.execute(sql_query, values)

for idx, row in top_transaction_district.iterrows():
    sql_query = "INSERT INTO top_transaction_district (State, Year, Quater, Total_district_transactions_no, Total_district_transactions_amount, District_name) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['Total_district_transactions_no'], row['Total_district_transactions_amount'], row['District_name'])
    cursor.execute(sql_query, values)

for idx, row in top_transaction_pincode.iterrows():
    sql_query = "INSERT INTO top_transaction_pincode (State, Year, Quater, Pincode, Total_pincode_transactions_no, Total_pincode_transactions_amount) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['Pincode'], row['Total_pincode_transactions_no'], row['Total_pincode_transactions_amount'])
    cursor.execute(sql_query, values)

for idx, row in top_user_district.iterrows():
    sql_query = "INSERT INTO top_user_district (State, Year, Quater, Total_district_registered_users, District_name) VALUES (%s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'], row['Total_district_registered_users'], row['District_name'])
    cursor.execute(sql_query, values)

for idx, row in top_user_pincode.iterrows():
    sql_query = "INSERT INTO top_user_pincode (State, Year, Quater,Total_pincode_registered_users, pincode) VALUES (%s, %s, %s, %s, %s)"
    values = (row['State'], row['Year'], row['Quater'],row['Total_pincode_registered_users'], row['pincode'])
    cursor.execute(sql_query, values)

# Commit the changes
conn.commit() 
