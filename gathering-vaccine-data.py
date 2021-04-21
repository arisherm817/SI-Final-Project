from bs4 import BeautifulSoup
import json
import os
import requests
import sqlite3
import csv


#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 

# def set_up_database(name):
#     path = os.path.dirname(os.path.abspath(__file__))
#     conn = sqlite3.connect(path + '/' + name)
#     cur = conn.cursor()
#     return cur, conn

def get_vaccine_data():
    data = {}
    url = 'https://en.wikipedia.org/wiki/Deployment_of_COVID-19_vaccines'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find('div', id = 'covid19-container')
    table = divs.find('table')
    trs = table.find_all('tr')
    for i in trs[3:]: 
        tds = i.find_all('td')
        td = tds[0]
        name = td.find('a')
        country = name.text.strip()
        number = tds[2]
        percent = number.text.strip('%')
        data[country] = percent
    print(data)

    # for i in trs: 
    #     country = i.find('td', class_ = 'entity sorted')
    #     name = country.text.strip()
    #     percent_row = i.find('td', class_ = 'dimension dimension-end')
    #     percent = int(percent_row.text.strip('%'))
    #     data[name] = percent
    # print(data)
    #d = soup.find_all('div', class_ = 'covid19-container')
    

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