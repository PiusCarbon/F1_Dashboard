import streamlit as st
import fastf1
import matplotlib.pyplot as plt
import plotly.express as px

def get_gps_of_year(year: int):
    event_schedule = fastf1.get_event_schedule(year)
    gp_list = list(event_schedule["EventName"].iloc[1:])
    return gp_list

def get_colors_of_compounds(tyres: list) -> list:
    color_dict = {
        "SOFT": "red",
        "MEDIUM": "yellow",
        "HARD": "white",
        "INTERMEDIATE": "green",
        "WET": "blue"
    }
    colors = []
    for i in range(0, len(tyres)):
        colors.append(color_dict[tyres[i]])
    return colors

st.header("tyre strategies")
st.write("This page provides you with data about the different Tyre Compounds used by drivers in the race. The drivers are ordered by their position at the end of the race.")

col1, col2, col3 = st.columns(3)
with col1:
    year = st.selectbox("Select Season", options=range(2019, 2023), help="Choose a season. The API supports only the seasons 2019-2022")
with col2:
    gp =    st.selectbox("Select Grand Prix", options=get_gps_of_year(year))
search = st.button("Search")

if search == True:
    race = fastf1.get_session(year, gp, 'R')
    race.load()

    x = []
    y = []
    c = []
    tyres = list(race.laps["Compound"].unique())
    color_sequence = get_colors_of_compounds(tyres)

    # for driver, index in zip(race.laps["DriverNumber"].unique(), range(0, len(race.laps["DriverNumber"].unique()))):
    #     df_driver = race.laps[race.laps["DriverNumber"]==driver]
    #     for _, row in df_driver.iterrows():
    #         x.append(driver)
    #         y.append(row["LapNumber"])
    #         c.append(tyres.index(row["Compound"]))

    # fig, ax = plt.subplots()
    # ax.scatter(y, x, c=c)
    # ax.set_xlabel("Laps")
    # ax.set_ylabel("Drivers")
    # ax.legend()
    # st.pyplot(fig
    cat_order = race.results["Abbreviation"]
    fig1 = px.scatter(race.laps, x="LapNumber", y="Driver", color="Compound", color_discrete_sequence=color_sequence, category_orders=cat_order)
    fig1.update_layout(plot_bgcolor='rgb(10,10,10)')
    st.plotly_chart(fig1)
    