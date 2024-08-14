# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import pandas as pd
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!!
    """
)
cnx=st.connection("snowflake")
session=cnx.session()
name_on_order=st.text_input("name on smoothie")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'),col('search_on'))
pd_df=my_dataframe.to_pandas()
ingredients_list=st.multiselect('Choose maximum of 5 fruits',my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string='';
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' ';
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', each_fruit,' is ', search_on, '.')
        st.subheader( each_fruit+ 'Nutrient_Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+search_on)
        fv_dataframe = st.dataframe(data=fruityvice_response.json(),use_container_width=True)
    sql_insert="""insert into smoothies.public.orders(ingredients,name_on_order) values('"""+ingredients_string+"""' , '"""+name_on_order+"""')""";
    submit_button=st.button('submit order');
    if submit_button:
        session.sql(sql_insert).collect()
        st.success(' Your Smoothie is ordered '+name_on_order+' !', icon="✅");

        





