import plotly.graph_objects as go
import plotly.express as px
import requests
import re
import os
import csv
import sqlite3
import json

#The Effect of Covid-19 on Uber Times and Prices
#Team members: Lindsay Brenner and Ari Sherman 


def main():

    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/vaccine.db')
    cur = conn.cursor()

    cur.execute("SELECT Covid.country, VaccineTable.vaccinated, Covid.confirmed FROM VaccineTable LEFT JOIN Covid ON VaccineTable.country = Covid.country") 
    results = cur.fetchall()
    conn.commit()

    data = {}
    for country in results: 
        if type(country[1]) != int or type(country[2]) != int or type(country[0]) != str: 
            continue
        else: 
            #(Confirmed, Vaccinated)
            data[country[0]] = (country[2], country[1])

    
    countries_list = []
    confirmed_list = []
    vaccinated_list = []

    for i in data:
        countries_list.append(i)
        confirmed_list.append(data[i][0])
        vaccinated_list.append(data[i][1])

    cur.execute('SELECT country, confirmed, deaths FROM Covid')
    data1 = cur.fetchall()
    death_rate_list = []
    for country in data1: 
        if country[2] == 0: 
            continue 
        else: 
            death_rate = (country[2]/country[1])
            new = (country[0], round(death_rate, 3))
            death_rate_list.append(new)
    sorted_death_rate_list = sorted(death_rate_list, key = lambda x: x[1], reverse = True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=confirmed_list,
        y=vaccinated_list,
        marker=dict(color="blue", size=8),
        mode="markers", 
        text = countries_list, 
        textposition = 'top center'
    ))

    fig.update_layout(title = "Confirmed Cases vs. Number of Vaccinations",
                        xaxis_title="Confirmed Cases", yaxis_title="Number of Vaccinations")
    fig.update_xaxes(type='log')
    fig.update_yaxes(type='log')
    fig.show()


if __name__ == "__main__":
    main()