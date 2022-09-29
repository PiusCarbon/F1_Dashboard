import streamlit as st
import pandas as pd
import numpy as np
import fastf1
import matplotlib.pyplot as plt

st.header("Did the strategy work?")

def get_gps_of_year(year: int):
    event_schedule = fastf1.get_event_schedule(year)
    gp_list = list(event_schedule["EventName"].iloc[1:])
    return gp_list

col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Select Season", options=range(2019, 2023), help="Choose a season. The API supports only the seasons 2019-2022")
with col2:
    gp =    st.selectbox("Select Grand Prix", options=get_gps_of_year(year))
with col3:
    driver =    st.selectbox("Select Driver", options=get_gps_of_year(year))
search = st.button("Search")

if search == True:
    session = fastf1.get_session(year, gp, 'R')
    session.load()

DRIVER = 'VER'  # which driver; need to specify number and abbreviation
DRIVER_NUMBER = '33'
LAP_N = 10  # which lap number to plot

drv_laps = session.laps.pick_driver(driver)
drv_lap = drv_laps[(drv_laps['LapNumber'] == LAP_N)]  # select the lap

# create a matplotlib figure
fig = plt.figure()
ax = fig.add_subplot()

# ############### new
df_new = drv_lap.get_car_data().add_driver_ahead()
ax.plot(df_new['Time'], df_new['DistanceToDriverAhead'], label='new')

plt.legend()
st.pyplot(fig)

