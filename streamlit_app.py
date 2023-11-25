import streamlit
import requests
import pandas as pd
import snowflake.connector

#First menu section
streamlit.title("My Parent's New Healthy Diner!")
streamlit.header('Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

#Second menu section
streamlit.header('🍌🍊Build Your Own Fruit Smoothie🥝🍇')

#Read the csv that houses the information on fruit
my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')

#Replace the index with the fruit
my_fruit_list.set_index('Fruit', inplace=True)

#Insert multi-select so customers can pick their fruit(s) of choice
fruits_selected = streamlit.multiselect('Pick your fruits!', list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

#Dataframe of available fruits
streamlit.dataframe(fruits_to_show)

#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit Advice!')
fruit_choice = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}").json()

#Normalize the json response
fruityvice_normalized = pd.json_normalize(fruityvice_response) 
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute('SELECT * FROM fruit_load_list')
my_data_row = my_cur.fetchone()
streamlit.text('The fruit load list contains:')
streamlit.text(my_data_row)