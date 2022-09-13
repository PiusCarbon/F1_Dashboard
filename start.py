import streamlit as st
import fastf1

st.header("F1 page")
fastf1.Cache.enable_cache('fastf1_cache')

session = fastf1.get_session(2019, 'Monza', 'Q')
session.load()

session

ver_lap = session.laps.pick_driver('VER').pick_fastest()
ham_lap = session.laps.pick_driver('HAM').pick_fastest()

ver_tel = ver_lap.get_car_data().add_distance()
ham_tel = ham_lap.get_car_data().add_distance()


print(type(session))