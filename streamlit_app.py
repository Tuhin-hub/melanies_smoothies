# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col





# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """
    Choose the fruits you want in your custome Smoothie! 
    """
)

NAME_ON_ORDER=''
NAME_ON_ORDER=st.text_input("Name of your smoothie will be :")
if NAME_ON_ORDER:
        st.write("name of your smoothie!! :",NAME_ON_ORDER)


# Securely access Snowflake credentials from environment variables
user = os.environ.get("SNOWFLAKE_USER")
password = os.environ.get("SNOWFLAKE_PASSWORD")
account = os.environ.get("SNOWFLAKE_ACCOUNT")

# Connect to Snowflake using secure credentials
try:
    cnx = snowflake.connector.connect(
        user=user,
        password=password,
        account=account,
        # Other connection parameters
    )
    ss = cnx.cursor()
    # Use ss object for database interactions
except Exception as e:
    st.error(f"Connection failed: {e}")

cnx = st.connection("snowflake")
ss = cnx.session()  
Selected_fruite=''
if NAME_ON_ORDER != '' :

    FRUIT_NAME=ss.table("Smoothies.public.fruit_options").select(col("FRUIT_NAME"))
    Selected_fruite=st.multiselect ("Select your fruite",FRUIT_NAME, max_selections=5) 

##ss.sql("truncate table  SMOOTHIES.PUBLIC.ORDERS;").collect()





INGREDIENTS=''

if   Selected_fruite :
    ##st.write(Selected_fruite)
    ##st.text(Selected_fruite)
    
    ADD_in=st.button('Submit Order')
    if ADD_in :
            for X in Selected_fruite :
                if INGREDIENTS =='' :
                    INGREDIENTS=X
                else :
                 INGREDIENTS=INGREDIENTS+' '+X
        
            st.write("selected items are :" ,INGREDIENTS)
    
sql_insert=''

if INGREDIENTS :
    sql_insert=("""insert into SMOOTHIES.PUBLIC.ORDERS(INGREDIENTS,NAME_ON_ORDER)
                values('"""+INGREDIENTS+"','"+NAME_ON_ORDER+"""'
               );"""
                )
    sql_insert
    ss.sql(sql_insert).collect()       
    st.success("all smoothie is ordered "+NAME_ON_ORDER,icon="✅")


ORDERS=ss.table("SMOOTHIES.PUBLIC.ORDERS")##.select(col("NAME_ON_ORDER").getField()=NAME_ON_ORDER)

st.dataframe(data=ORDERS,use_container_width=True)
st.stop()

