# Import python packages
import streamlit as st
conn = st.connection("snowflake")
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothies!:cup_with_straw:")
st.write(
    """Choose the fruit you want in your custom smoothie.
    """
)

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name of your smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data = my_dataframe, use_container_width=True)

ingredients_list =  st.multiselect('Select 5 Ingridients:', my_dataframe,
                                  max_selections =5)

if ingredients_list:
    #st.write(ingridients_list)
    #st.text(ingridients_list)

    ingredients_string = ''

    for frutis_choosen in ingredients_list:
        ingredients_string += frutis_choosen+' '

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
                    values('"""+ingredients_string+"""','"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+' !', icon="✅")
