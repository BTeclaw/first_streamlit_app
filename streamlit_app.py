import streamlit 
import pandas as pd
import requests as rq
import snowflake.connector
from urllib import URLError




def get_fruityvice_data(fruit_choice_string):
    fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice_string)
    fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
    return fruityvice_normalized


def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall()

def insert_fruit_snowflake(new_fruit_string):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" + new_fruit_string +"')")
        return "Added " + new_fruit_string + "succesfully !"

streamlit.header("Fruityvice Fruit Advice")
try:
    fruit_choice = streamlit.text_input("What fruit would you like information about ?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
        streamlit.dataframe(get_fruityvice_data(fruit_choice))
except URLError as e:
    streamlit.error()



my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)



if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows= get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input("What fruit to add ?")
if streamlit.button("Add a Fruit to the list in Snowflake"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    streamlit.text(insert_fruit_snowflake(add_my_fruit))






