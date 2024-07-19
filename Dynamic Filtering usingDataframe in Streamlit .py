import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
df=pd.read_csv(r"C:\Users\DELL\RedBus_Routes.csv")
df['Start_time']= pd.to_datetime(df['Start_time'])
df.index=df['Start_time']
df['Bus_Route']=df['Starting_names']+" to "+df['Reaching_names']
Seattype=['Sleeper','Seater']
ACtype=['AC','NON AC']
Start_time=['1:00 - 2:00','2:00 - 3:00','3:00 - 4:00','4:00 - 5:00','5:00 - 6:00','6:00 - 7:00','7:00 - 8:00','8:00 - 9:00','9:00 - 10:00','10:00 - 11:00','11:00 - 12:00','12:00 - 13:00','13:00 - 14:00','14:00 - 15:00','15:00 - 16:00','16:00 - 17:00','17:00 - 18:00','18:00 - 19:00','20:00 - 21:00','21:00 - 22:00','22:00 - 23:00','23:00 - 23:59']
Ratings=['1 - 2','2 - 3','3 - 4','4 - 5','2 - 4','3 - 5']
with st.sidebar:
    selected=option_menu(menu_title="Menu",options=['Home','Select Bus'],menu_icon='house')
if selected == "Home":
    st.title("Welcome to Red Bus Online Booking!")
if selected == "Select Bus":
    col1,col2,col3= st.columns(3)
    col4,col5,col6=st.columns(3)
    with col1:
        Bus_Route = st.selectbox(    
                "Select the route",    
                options=df['Bus_Route'].unique()    
            )
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
        df = df[df["Bus_Route"]==Bus_Route]
    if Seat:
        if Seat=="Seater":
            df = df[df["Bus_Type"].str.contains(Seat,case=False) | df["Bus_Type"].str.contains(' Semi Sleeper',case=False) | ~df["Bus_Type"].str.contains('Sleeper',case=False)]
        else:
            df = df[df["Bus_Type"].str.contains(Seat,case=False) & ~df["Bus_Type"].str.contains('Semi Sleeper',case=False)] 
    if ACtypes:
        if ACtypes=='AC':
            df = df[df["Bus_Type"].str.contains(ACtypes,case=False) & ~df['Bus_Type'].str.contains('NON AC',case=False)]
        else:
            df = df[df["Bus_Type"].str.contains(ACtypes,case=False)]
    if Star_Rating:
        b=[]
        b=Star_Rating.split(" ")
        S=int(b[0])
        E=int(b[2])
        df = df[df["Star_Ratings"].between(S,E)] 
    if Start_Time:
        a=[]
        a=Start_Time.split(" ")
        start=a[0]
        end=a[2]
        df=df.between_time(start,end)
    if Price:    
        df = df[df["Bus_fare"].between(Price[0], Price[1])]
    st.write(df)    

