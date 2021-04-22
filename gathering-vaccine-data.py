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
    sorted_dict = {}
    url = 'https://en.wikipedia.org/wiki/Deployment_of_COVID-19_vaccines'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    divs = soup.find('div', id = 'covid19-container')
    table = divs.find('table')
    trs = table.find_all('tr')
    for i in trs[2:193]: 
        tds = i.find_all('td')
        td = tds[0]
        name = td.find('a')
        country = name.text.strip()
        number = tds[2]
        percent = number.text.strip('%')
        number = (tds[1].text.replace(',', ''))
        if percent == '--' or country == "EU":
            continue
        else:
            data[country] = (float(percent), int(number))
    sorted_data = sorted(data.keys(), key = lambda x: data[x][1], reverse = True)
    for d in sorted_data[:125]:
        sorted_dict[d] = data[d]
    return sorted_dict
    

def fill_country_id_table(cur, conn): 
    cur.execute("CREATE TABLE IF NOT EXISTS CountryIds (country_id INTEGER PRIMARY KEY, country TEXT)")
    countries = get_vaccine_data()
    countries_list = []

    while len(countries_list) < len(countries):
        count = 0
        for country in countries:
                country_id = len(countries_list) + 1
                if country in countries_list:
                    continue
                else:
                    cur.execute("INSERT OR IGNORE INTO CountryIds (country_id, country) VALUES (?,?)", (country_id, country))
                    count += 1
                    countries_list.append(country)
                if count == 25:
                    break
    conn.commit()
    
def fill_vaccine_table(cur, conn): 
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineTable (country_id INTEGER PRIMARY KEY, vaccinated INTEGER, percent NUMBER)")
    countries = get_vaccine_data()
    countries_list = []

    while len(countries_list) < len(countries):
        count = 0
        for country in countries:
                country_id = len(countries_list) + 1
                if country in countries_list:
                    continue
                else:
                    cur.execute("INSERT OR IGNORE INTO VaccineTable (country_id, vaccinated, percent) VALUES (?,?,?)", (country_id, countries[country][1], countries[country][0]))
                    count += 1
                    countries_list.append(country)
                if count == 25:
                    break
    conn.commit()


def set_up_vaccine_tables(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS CountryIds (country_id INTEGER PRIMARY KEY, country TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineTable (country_id INTEGER PRIMARY KEY, vaccinated INTEGER, percent NUMBER)")
    conn.commit()

def calculate_average_percent_vaccinated(cur):
    cur.execute('SELECT percent FROM VaccineTable')
    percent_list = cur.fetchall()
    total_percent = 0
    num_countries = 0
    for p in percent_list:
        total_percent += p[0]
        num_countries += 1
    percent = (total_percent/num_countries)
    return round(percent, 2)

def write_data_file(filename, cur, conn):
    cur.execute('SELECT country FROM CountryIds')
    countries = cur.fetchall()
    if len(countries) == 100:

        path = os.path.dirname(os.path.abspath(__file__)) + os.sep

        outFile = open(path + filename, "w")
        outFile.write("Average Percent Vaccinated Per Country\n")
        outFile.write("=====================================================\n\n")
        percent = str(calculate_average_percent_vaccinated(cur))
        outFile.write(percent + "%" + "\n\n")
        outFile.write("Top Ten Highest Vaccination Percentages in the World\n")
        outFile.write("======================================================\n\n")
        outFile.write("1. " + str(countries[0][0]) + "\n")
        outFile.write("2. " + str(countries[1][0]) + "\n")
        outFile.write("3. " + str(countries[2][0]) + "\n")
        outFile.write("4. " + str(countries[3][0]) + "\n")
        outFile.write("5. " + str(countries[4][0]) + "\n")
        outFile.write("6. " + str(countries[5][0]) + "\n")
        outFile.write("7. " + str(countries[6][0]) + "\n")
        outFile.write("8. " + str(countries[7][0]) + "\n")
        outFile.write("9. " + str(countries[8][0]) + "\n")
        outFile.write("10. " + str(countries[9][0]) + "\n")
        outFile.close()

def main():
    cur, conn = set_up_database('vaccine.db')
    set_up_vaccine_tables(cur, conn)
    fill_country_id_table(cur, conn)
    fill_vaccine_table(cur,conn)
    write_data_file("vaccine_data.txt", cur, conn)
    conn.close()


if __name__ == "__main__":
    main()