# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col 
import time
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie!")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)


# At the top of your script, before the widgets:
if 'submitted' not in st.session_state:
    st.session_state['submitted'] = False

if st.session_state['submitted']:
    st.session_state['submitted'] = False
    st.session_state['name_on_order'] = ''
    st.session_state['ingredients'] = []
    # st.rerun()

name_on_order = st.text_input('Name on Smoothie: ',
                             key='name_on_order')
if name_on_order:
    st.write("The name on your Smoothie will be: {}".format(name_on_order))

# (Before) session = get_active_session()
# (After)
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options") \
                      .select(col('FRUIT_NAME'))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients", 
    my_dataframe,
    max_selections = 5,
    key = 'ingredients'
)
if ingredients_list:
    ingredients_string = "  ".join(ingredients_list)
    
    st.write("You ordered: {}".format(ingredients_string))

time_to_insert = st.button("Submit Order")
if time_to_insert:
    my_insert_stmt = """ insert into smoothies.public.orders
                        (name_on_order, ingredients)
                        values ('{}', '{}')
                        """.format(name_on_order, ingredients_string)
    # st.write(my_insert_stmt)
    session.sql(my_insert_stmt).collect()
    st.success('Your smoothie is ordered!', icon="✅")
    st.session_state['submitted'] = True 
    time.sleep(3)
    st.rerun()
  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
# st.text(smoothiefroot_response.json())
sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
