import plotly.graph_objects as go
import plotly.express as px
import requests
import re
import os
import csv
import sqlite3
import json

#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 


def main():
    """ Takes in no inputs and returns nothing. Fetches data from the vaccine database and loads the information into lists. Usings the imputed python package, plotly to create a scatterplot of confirmed cases vs. number of vaccinations per country and a barplot of the ten countries with the highest death rates. """
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/vaccine.db')
    cur = conn.cursor()

    cur.execute("SELECT VaccineNumberTable.country, VaccineNumberTable.vaccinated, Covid.confirmed FROM VaccineNumberTable LEFT JOIN Covid ON VaccineNumberTable.country_id = Covid.country_id") 
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

    cur.execute('SELECT country_id, confirmed, deaths FROM Covid')
    data1 = cur.fetchall()
    death_rate_list = []
    for country in data1: 
        if country[2] == 0: 
            continue 
        else: 
            death_rate = (country[2]/country[1])
            statement = "SELECT country FROM VaccineNumberTable WHERE country_id = {}".format(country[0])
            cur.execute(statement)
            country1 = cur.fetchone()[0]
            new = (country1, round(death_rate, 3))
            death_rate_list.append(new)
    sorted_death_rate_list = sorted(death_rate_list, key = lambda x: x[1], reverse = True)
    top_countries = []
    deaths = []
    for i in sorted_death_rate_list[:10]: 
        top_countries.append(i[0])
        deaths.append(i[1])
    

    figure = go.Figure()
    figure.add_trace(go.Scatter(
        x=confirmed_list,
        y=vaccinated_list,
        marker=dict(color="blue", size=8),
        mode="markers", 
        text = countries_list, 
        textposition = 'top center'
    ))

    figure.update_layout(title = "Confirmed Cases vs. Number of Vaccinations",
                        xaxis_title="Confirmed Cases", yaxis_title="Number of Vaccinations")
    figure.update_xaxes(type='log')
    figure.update_yaxes(type='log')
    figure.show()

    bar_chart_figure = go.Figure([go.Bar(y = deaths, x = top_countries)])
    bar_chart_figure.update_traces(marker_color="lightskyblue", marker_line_color="royalblue", marker_line_width=3, opacity=.9)
    bar_chart_figure.update_layout(title_text = "Top Ten Covid Death Rates", xaxis_title="Country", yaxis_title="Death Rate")
    bar_chart_figure.show()


if __name__ == "__main__":
    main()