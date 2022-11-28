import streamlit as st
import pandas as pd
import numpy as np
import csv
from datetime import datetime
from itertools import groupby


LOOKUP_SEASON = {
    11: 'November',
    12: 'December',
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October'
}

def get_season(row):
    date = datetime.strptime(row[0], '%m/%d/%Y')
    season = LOOKUP_SEASON[date.month]
    return season + " " + str(date.year)

def get_season_num(row):
    date = datetime.strptime(row[0], '%m/%d/%Y')
    return date.month

def get_year(row):
    date = datetime.strptime(row[0], '%m/%d/%Y')
    return date.year

st.title("Purchased Books Graphing Tool")

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
    shows = pd.read_csv("PurchaseDates.csv")
    file_container.write(shows)

c29, c30, c31 = st.columns([1, 6, 1])
with c30:
    clicked = st.button("graph")
    if clicked:
        file_container = st.expander("Check your generated graph")
        mean_data = []
        with open("PurchaseDates.csv") as data_file:
            reader = csv.reader(data_file)
            for year, seasons in groupby(reader, get_year):
                for season_str, iter_data in groupby(seasons, get_season):
                    data = list(iter_data)
                    mean = sum([float(row[1]) for row in data])
                    mean_data_entry = [season_str, mean]
                    mean_data.append(mean_data_entry)    
        chart_data = pd.DataFrame(mean_data,columns =['Season', 'Books Sold'])
        chart_data = chart_data.rename(columns={'Season':'index'}).set_index('index')
        st.bar_chart(chart_data["Books Sold"])
        st.caption("This graph displays the total books sold in each month in the past 4 years, grouped by month and year.")