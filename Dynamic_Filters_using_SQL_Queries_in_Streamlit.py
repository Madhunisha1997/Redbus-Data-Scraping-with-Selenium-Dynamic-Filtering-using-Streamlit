import pandas as pd
import mysql.connector as sql
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
column=[]
db_connection = sql.connect(host='localhost', database='MDE92', user='root', password='root')
db_cursor = db_connection.cursor()
Seattype=['Seater','Sleeper']
ACtype=['AC','NON AC']
Start_time=['1:00 - 2:00','2:00 - 3:00','3:00 - 4:00','4:00 - 5:00','5:00 - 6:00','6:00 - 7:00','7:00 - 8:00','8:00 - 9:00','9:00 - 10:00','10:00 - 11:00','11:00 - 12:00','12:00 - 13:00','13:00 - 14:00','14:00 - 15:00','15:00 - 16:00','16:00 - 17:00','17:00 - 18:00','18:00 - 19:00','20:00 - 21:00','21:00 - 22:00','22:00 - 23:00','23:00 - 23:59']
Ratings=['1 - 2','2 - 3','3 - 4','4 - 5','2 - 4','3 - 5']
db_cursor.execute('SELECT route_name FROM Red_Bus_routes')
Route_Name=db_cursor.fetchall()
df=pd.DataFrame(Route_Name,columns=['Bus_routes_names'])
with st.sidebar:
    selected=option_menu(menu_title="Menu",options=['Home','Select Bus'],menu_icon='house')
if selected == "Home":
    st.title("Welcome to Red Bus Online Booking!")
if selected == "Select Bus":
    col1,col2,col3= st.columns(3)
    col4,col5,col6= st.columns(3)
    with col1:
        Bus_Route = st.selectbox(    
                    "Select the route",    
                options=df['Bus_routes_names'].unique() )
    with col2:
        Seat = st.selectbox(    
                "Select the Seat Type",    
                options=Seattype    
            ) 
    with col3:
        ACtypes = st.selectbox(    
                "Select the AC Type",    
                options=ACtype    
            ) 
    with col4:
        Star_Rating=st.selectbox(
                "Select the Rating",
                options=Ratings
            )
    with col5:
        Start_Time = st.selectbox(    
                "Select the Starting Time",    
                options= Start_time   
            )
    with col6:
        Price = st.slider("Select the Bus Fare range", 0, 5000, (0, 1000))
    if Bus_Route:
        query=('create or replace view table1 as SELECT * FROM Red_Bus_routes where route_name=%s')
        data=(Bus_Route,)
        db_cursor.execute(query,data)
        db_cursor.execute('select * from table1')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)
    if Seat:
        if Seat=="Seater":
             query="create or replace view table2 as SELECT * FROM table1 where (upper(Bus_Type) LIKE %s) or (UPPER(Bus_Type) LIKE '%SEMI SLEEPER%') or (UPPER(Bus_Type) NOT LIKE '%SLEEPER%')"
             data=('%'+Seat.upper()+'%',)
             db_cursor.execute(query,data)
        else:
             query=("create or replace view table2 as SELECT * FROM table1 where (UPPER(Bus_Type) LIKE %s) & (UPPER(Bus_Type) NOT LIKE '%SEMI SLEEPER%')")
             data=('%'+Seat.upper()+'%',)
             db_cursor.execute(query,data)
        db_cursor.execute('select * from table2')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)
    if ACtypes:
        if ACtypes=='AC':
            query=("create or replace view table3 as SELECT * FROM table2 where (Bus_Type LIKE %s) & (Bus_Type NOT LIKE '%NON AC%')")
            data=('%'+ACtypes+'%',)
            db_cursor.execute(query,data)
        else:
            query=("create or replace view table3 as SELECT * FROM table2 where (Bus_Type LIKE %s)")
            data=('%'+ACtypes+'%',)
            db_cursor.execute(query,data)
        db_cursor.execute('select * from table3')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)
    if Star_Rating:
        b=[]
        b=Star_Rating.split(" ")
        start=int(b[0])
        end=int(b[2])
        query=('create or replace view table4 as select * from table3 where Star_rating between %s and %s')
        data=(start,end)
        db_cursor.execute(query,data)
        db_cursor.execute('select * from table4')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)     
    if Start_Time:
        a=[]
        a=Start_Time.split(" ")
        start=a[0]
        end=a[2]
        query=('create or replace view table5 as select * from table4 where time(departing_time) between %s and %s')
        data=(start,end)
        db_cursor.execute(query,data)
        db_cursor.execute('select * from table5')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)
    if Price: 
        query=('create or replace view table6 as select * from table5 where price between %s and %s')
        data=(Price[0],Price[1])
        db_cursor.execute(query,data)
        db_cursor.execute('select * from table6')
        Table=db_cursor.fetchall()
        df=pd.DataFrame(Table)   
    df.columns=['ID','STARTING_NAMES','REACHING_NAMES','BUS_ROUTE_LINKS','BUS_NAME','BUS_TYPES','STARTING_NAMES','DURATION','REACHING_TIME','STAR_RATING','BUS_FARE','SEATS_AVAILABLE','BUS_ROUTES']
    #df.columns=column
    st.write(df)



