from types import resolve_bases
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import fastf1
import plotly.express as px

results_path = os.path.join(os.getcwd(), "results_cache")

def get_gps_of_year(year: int):
    gp_list = []
    event_schedule = fastf1.get_event_schedule(year)
    gp_list = list(event_schedule["EventName"].iloc[1:])
    gp_list
    return gp_list

def accumulate_points_per_season(season_df: pd.DataFrame):
    
    # 1. Driver
    season_df1 = season_df.sort_values(["Driver", "GP"])
    points = np.zeros([len(season_df), 1])
    prev_driver = ""

    for index, row in season_df1.iterrows():
        if prev_driver != row["Driver"]:
            total_points = row["Points"]
        else:
            total_points += row["Points"]
        points[index] = total_points
        prev_driver = row["Driver"]
    
    season_df["Acc Driver Points"] = points

    # 2. Team
    season_df2 = season_df.sort_values(["Team", "GP"])
    team_points = np.zeros([len(season_df), 1])
    prev_team = ""

    for index, row in season_df2.iterrows():
        if prev_team != row["Team"]:
            total_points = row["Points"]
        else:
            total_points += row["Points"]
        team_points[index] = total_points
        prev_team = row["Team"]
    
    season_df["Acc Team Points"] = team_points

    return season_df

def accumulate_relative_points_total_df(df: pd.DataFrame):
    
    # 1. Driver
    df = df.reset_index()
    df1 = df.sort_values(["Driver", "GP"])
    points = np.zeros([len(df), 1])
    prev_driver = ""

    for index, row in df1.iterrows():
        if prev_driver != row["Driver"]:
            total_points = row["Relative Driver Points"]
        else:
            total_points += row["Relative Driver Points"]
        points[index] = total_points
        prev_driver = row["Driver"]

    df["Relative Acc Driver Points"] = points

    # 2. Team
    df2 = df.sort_values(["Team", "GP"])
    team_points = np.zeros([len(df), 1])
    prev_team = ""

    for index, row in df2.iterrows():
        if prev_team != row["Team"]:
            total_points = row["Relative Driver Points"]
        else:
            total_points += row["Relative Driver Points"]
        team_points[index] = total_points
        prev_team = row["Team"]
    
    df["Relative Acc Team Points"] = team_points

    return df

def reward_relative_points(df: pd.DataFrame):

    # check if function already performed on DataFrame
    if "Relative Driver Points" in df.columns:
        print("function is already applied on this dataframe")
        return df_total

    first = True
    for year in df["Year"].unique():
    
        df_year = df[df["Year"]==year]
        df_year["Relative Driver Points"] = df_year["Points"] / df_year["Points"].sum()

        if first == True:
            df_total = df_year
            first = False
        else: 
            df_total = pd.concat([df_total, df_year], axis=0)

    df_total = accumulate_relative_points_total_df(df_total)
        
    return df_total

def points_over_multiple_seasons(seasons_list_names: list):
    
    first = True
    total_GPs = 0
    
    for name_of_df in seasons_list_names:
        
        df_season = pd.read_csv(os.path.join(results_path, name_of_df))
        
        if first == True:
            df_season = accumulate_points_per_season(df_season)
            df_total = df_season
            first = False
        else:
            df_season = accumulate_points_per_season(df_season)
            df_season["GP"] = df_season["GP"] + total_GPs
            df_total = pd.concat([df_total, df_season], axis=0)

        total_GPs = df_season["GP"].max()

    df_rewarded = reward_relative_points(df_total)
    
    return df_rewarded

def get_year_slider_values(path):
    
    years_list = []
    
    for file in os.listdir(path):
        y = file.split("results")[1].split(".csv")[0]
        years_list.append(y)
    
    return [int(min(years_list)), int(max(years_list))]

def years_to_dataframe_names(years: list):
    
    dataframe_names = []
    
    for y in years:
        dataframe_names.append("results" + str(y) + ".csv")
    
    return dataframe_names


##################
##################
## Seitenbeginn ##
##################
##################
st.header("Championship points over time")

year_min, year_max = st.slider("year", get_year_slider_values(results_path)[0], get_year_slider_values(results_path)[1], (get_year_slider_values(results_path)[0], get_year_slider_values(results_path)[1]))

sc1, sc2 = st.columns(2)
with sc1:
    instance = st.radio("Show championship points of", options=["Driver", "Team"])
    log = st.radio("Plot with logarithmic y scale?", options=[False, True])
    show_plot = st.button("show plot")
with sc2:
    rel_abs = st.radio("Relative or absolute points?", options=["Absolute", "Relative"])
    acc = st.radio("Accumulate points?", options=["Yes", "No"])

df = points_over_multiple_seasons(years_to_dataframe_names(range(year_min, year_max+1)))

if rel_abs == "Relative":
    if acc == "Yes":
        if instance == "Driver":
            fig = px.line(df, x="GP", y="Relative Acc Driver Points", color=instance, log_y=log)
        else:
            fig = px.line(df, x="GP", y="Relative Acc Team Points", color=instance, log_y=log)
    else:
        fig = px.line(df, x="GP", y="Relative Driver Points", color=instance, log_y=log)
else:
    if acc == "Yes":
        if instance == "Driver":
            fig = px.line(df, x="GP", y="Acc Driver Points", color=instance, log_y=log)
        else:
            fig = px.line(df, x="GP", y="Acc Team Points", color=instance, log_y=log)
    else:
        fig = px.line(df, x="GP", y="Points", color=instance, log_y=log)

if show_plot == True:
    st.plotly_chart(fig)