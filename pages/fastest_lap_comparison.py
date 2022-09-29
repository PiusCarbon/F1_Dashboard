import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import time

def get_gps_of_year(year: int):
    event_schedule = fastf1.get_event_schedule(year)
    gp_list = list(event_schedule["EventName"].iloc[1:])
    return gp_list

st.header("Fastest Lap Comparisons")

col1, col2 = st.columns(2)
with col1:
    year = st.selectbox("year", options=range(2018, 2022))
with col2:
    gp = st.selectbox("gp", options=get_gps_of_year(year))
search = st.button("Search for Drivers")

drivers = []

if search == True:
    session = fastf1.get_session(year, gp, 'Q')
    session.load()
    for d in list(session.laps["Driver"].unique()):
        drivers.append(d)

col1, col2 = st.columns(2)
with col1:
    driver1 = st.selectbox("driver 1", options=drivers)
with col2:
    driver2 = st.selectbox("driver 2", options=drivers)
plot = st.button("Plot fastest Lap")

if plot == True:
    try:
        fast_leclerc = session.laps.pick_driver(driver1).pick_fastest()
        lec_pos_data = fast_leclerc.get_pos_data()

        fast_ham = session.laps.pick_driver(driver2).pick_fastest()
        ham_pos_data = fast_ham.get_pos_data()

        with st.empty():
            t = st.slider(0, min(len(lec_pos_data), len(ham_pos_data)))
            fig, ax = plt.subplots()
            ax.scatter(lec_pos_data["X"], lec_pos_data["Y"], color="black")
            x1 = lec_pos_data["X"][t]
            y1 = lec_pos_data["Y"][t]
            x2 = ham_pos_data["X"][t]
            y2 = ham_pos_data["Y"][t]
            ax.scatter(x1, y1, label="Lec")
            ax.scatter(x2, y2, label="Ham")
            ax.legend()
            st.write("Seconds:", t, "Distance:", np.sqrt((x1-x2) ** 2 + (y1-y2) ** 2), "meters")
            st.pyplot(fig)

    except:
        st.write("No data, sorry!")