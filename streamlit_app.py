# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your Smoothie!!
    """
)
session = get_active_session()
name_on_order=st.text_input("name on smoothie")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('Fruit_name'))
ingredients_list=st.multiselect('Choose maximum of 5 fruits',my_dataframe,max_selections=5)
if ingredients_list:
    ingredients_string='';
    for each_fruit in ingredients_list:
        ingredients_string+=each_fruit+' ';
    st.write(ingredients_string);
    sql_insert="""insert into smoothies.public.orders(ingredients,name_on_order) values('"""+ingredients_string+"""','"""+name_on_order+"""')""";
    st.write(sql_insert);
    submit_button=st.button('submit order');
    if submit_button:
        session.sql(sql_insert).collect()
        st.success(' Your Smoothie is ordered '+name_on_order+' !', icon="✅");
        





