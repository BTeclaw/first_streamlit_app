import streamlit 
import pandas as pd
import requests as rq
import snowflake.connector



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.text("The fruit load list contains: ")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input("What fruit to add ?")
streamlit.write("User entered", add_my_fruit)
my_data_rows.append(add_my_fruit)

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)


fruit_choice = streamlit.text_input("What fruit would you like information about ?", "Kiwi")
streamlit.write("User entered", fruit_choice)

fruityvice_response = rq.get("https://fruityvice.com/api/fruit/" + fruit_choice)
fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)