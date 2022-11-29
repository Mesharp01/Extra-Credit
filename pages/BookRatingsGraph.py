import streamlit as st
import pandas as pd
import numpy as np
import csv
from datetime import datetime
from itertools import groupby




def get_rating(row):
    rating = row[0]
    
    return rating

def get_num_books(row):
    numBooks = row[1]
    return numBooks



  
st.title("Book Ratings Graphing Tool")

def _max_width_():
    max_width_str = f"max-width: 1800px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )

c29, c30, c31 = st.columns([1, 6, 1])

with c30:
    file_container = st.expander("View .csv file")
    shows = pd.read_csv("BookRatings.csv") #REPLACE FILE HERE
    file_container.write(shows)

c29, c30, c31 = st.columns([1, 6, 1])
with c30:
    clicked = st.button("graph")
    if clicked:
        file_container = st.expander("Check your generated graph")
        mean_data = []
        with open("BookRatings.csv") as data_file:
            reader = csv.reader(data_file)
            for rating in reader:

                    entry = [rating[0], rating[1]]
                    mean_data.append(entry)    
        chart_data = pd.DataFrame(mean_data,columns =['Rating', 'Number of Books'])
        chart_data = chart_data.rename(columns={'Rating':'index'}).set_index('index')
        st.bar_chart(chart_data["Number of Books"])
        #pd.DataFrame.set_axis(xlabel = 'Rating', ylabel = 'Number of Books')
        st.caption("Displays number of books that achieved a certain rating")