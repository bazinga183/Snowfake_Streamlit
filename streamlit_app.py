import streamlit
import pandas as pd

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