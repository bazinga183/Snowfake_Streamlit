import streamlit
import pandas as pd
import snowflake.connector
from urllib.error import URLError

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
#Try to illicit a response from the user and only run once the user inputs a response
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error('Please select a fruit to get information.')
    else:    
        fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}").json()

        #Normalize the json response
        fruityvice_normalized = pd.json_normalize(fruityvice_response) 
        streamlit.dataframe(fruityvice_normalized)
except URLError as e:
    streamlit.error()

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute('SELECT * FROM fruit_load_list')
my_data_rows = my_cur.fetchall()
streamlit.header('The fruit load list contains:')
streamlit.dataframe(my_data_rows)

#Adding a fruit to the dataframe above
add_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write(f'Thanks for adding {add_fruit}!')

my_cur.execute('INSERT INTO fruit_load_list VALUES ("from streamlit)')