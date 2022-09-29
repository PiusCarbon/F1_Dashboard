import streamlit as st
import fastf1
import pandas as pd
from fastf1 import plotting
from matplotlib import pyplot as plt

st.header("F1 Dashboard")
st.write("Welcome to the F1 Dashboard. Feel free to explore the stats of F1")
st.subheader("How does this site work?")
st.write("See the pages listed on the top left corner? Click one of them to access a specific F1 stat you want to know more about")
st.write("Here is a quick overview what you can discover:")
st.write("**Championship points:** discover the points of drivers and teams for all seasons since 1950")
st.write("**Fastest Lap Comparison:** compare two drivers on their fastest lap in qualifying")
st.write("**Race Results:** Who was on the podium at the Monaco Grand Prix in 1978? Find it out")
st.write("**Tyre Strategies:** F1 is all about the tyres. Which compound did drivers choose in a GP?")

st.subheader("Support Me")
st.write("If you enjoy this site, please support me on Patreon. Every donation helps me to improve my content further!")