from bs4 import BeautifulSoup
import json
import os
import requests
import sqlite3
import csv


#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 

def set_up_database(name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + name)
    cur = conn.cursor()
    return cur, conn

def get_vaccine_data():
    data = {}
    url = 'https://ourworldindata.org/explorers/coronavirus-data-explorer?tab=table&zoomToSelection=true&time=2020-03-01..latest&pickerSort=desc&pickerMetric=total_vaccinations_per_hundred&Metric=Vaccine+doses&Interval=Cumulative&Relative+to+Population=true&Align+outbreaks=false&country=USA~GBR~ISR~DEU~ARE~ARG~FRA'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    a = soup.find_all('div', class_ = 'Explorer')
    b = a[0].find_all('tr')

    for i in trs: 
        country = i.find('td', class_ = 'entity sorted')
        name = country.text.strip()
        percent_row = i.find('td', class_ = 'dimension dimension-end')
        percent = int(percent_row.text.strip('%'))
        data[name] = percent
    print(data)
    

def fill_table(cur, conn): 
    pass

def set_up_vaccine_table(cur, conn):
    pass

def write_data_file(filename, cur, conn):
    pass

def main():
    get_vaccine_data()

    # cur, conn = set_up_database('vaccine.db')
    # set_up_vaccine_table(cur, conn)
    # fill_table(cur, conn)
    
    # write_data_file("vaccine-data.txt", cur, conn)
    # conn.close()


if __name__ == "__main__":
    main()