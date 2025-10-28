# secure_check_project
SecureCheck: A Python-SQL Digital Ledger for Police Post Logs

install import pandas as pd. 
save the file as csv file and read the file and save in the variable df.
next is to read and clean the data by following steps.
checking duplicates in df and droping if any.
seeing df info and changed the datatype of data and time from object.
checking the null values and fill the existed null values into unknown by fillna
because the nan values in data cannot be processed.
then connecting with mysql,
install and import mysql.connector.
created a database called secure_check in mysql,
use the database and create a table.
enter the column names and insert the data.
install and import streamlit as st,
created a connection by fetch_data from sql to streamlit.
created a side bar navigation and named the pages.
setting first page as introduction and updated some information and image,
created a second page as data visuals and placed the dataframe 
then created a visual sight by bar by importing plotly.express as px,
setting third page as sql queries, where all the queries given solved in mysql are displayed
by selecting the key the values will display ,
created a forth page as smart filter panel by which applying the filters a prediction summary will come as a output,
last page as created information.

