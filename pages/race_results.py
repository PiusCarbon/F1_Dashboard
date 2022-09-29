import streamlit as st
import fastf1
import pandas as pd
from fastf1 import plotting
from matplotlib import pyplot as plt

st.header("Race Results")
st.write("Welcome to the F1 Dashboard. Feel free to explore the stats of F1")

def get_gps_of_year(year: int):
    event_schedule = fastf1.get_event_schedule(year)
    gp_list = list(event_schedule["EventName"].iloc[1:])
    return gp_list

col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Select Season", options=range(2019, 2023), help="Choose a season. The API supports only the seasons 2019-2022")
with col2:
    gp =    st.selectbox("Select Grand Prix", options=get_gps_of_year(year))
search = st.button("Search")

if search == True:
    race = fastf1.get_session(year, gp, 'R')
    race.load()
    results = race.results
    print(results.head())
    st.write("Results:")
    st.dataframe(results["FullName"])