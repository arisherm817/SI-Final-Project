from bs4 import BeautifulSoup
import json
import os
import requests
import sqlite3
import csv


#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 

def set_up_database(name):
    """Takes in the name of a database an input and returns the cursor and connection to the database."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/' + name)
    cur = conn.cursor()
    return cur, conn

def get_vaccine_data():
    """Returns a dictionary with the key being the name of the country and the value being a tuple in the format (Percent Vaccinated, Total Vaccinations). """
    """Uses BeautifulSoup to read the countries name, the countries percent vaccinated, and total vaccinations"""
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
    for d in data:
        if d in sorted_data[:125]:
            sorted_dict[d] = (data[d], sorted_data.index(d)+1)
    return sorted_dict
    

def fill_country_rank_table(cur, conn): 
    """ Fills the Country Ranks table with the country names and their ranking for total number of vaccinations"""
    cur.execute("CREATE TABLE IF NOT EXISTS CountryRanks (country TEXT PRIMARY KEY, rank INTEGER)")
    countries = get_vaccine_data()
    countries_list = []

    while len(countries_list) < len(countries):
        count = 0
        for country in countries:
                if country in countries_list:
                    continue
                else:
                    cur.execute("INSERT OR IGNORE INTO CountryRanks (country, rank) VALUES (?,?)", (country, countries[country][1]))
                    count += 1
                    countries_list.append(country)
                if count == 25:
                    break
    conn.commit()
    
def fill_vaccine_table(cur, conn): 
    """ Fills the Vaccine Table table with the country names, the total number of vaccinations in the country, and the percent of the country population that is vaccinated"""
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineTable (country TEXT PRIMARY KEY, vaccinated INTEGER, percent NUMBER)")
    countries = get_vaccine_data()
    countries_list = []

    while len(countries_list) < len(countries):
        count = 0
        for country in countries:
                if country in countries_list:
                    continue
                else:
                    cur.execute("INSERT OR IGNORE INTO VaccineTable (country, vaccinated, percent) VALUES (?,?,?)", (country, countries[country][0][1], countries[country][0][0]))
                    count += 1
                    countries_list.append(country)
                if count == 25:
                    break
    conn.commit()


def set_up_vaccine_tables(cur, conn):
    """Creates two tables. One table that contain the country vaccination rankings and another table that has vaccine data for each country """
    cur.execute("CREATE TABLE IF NOT EXISTS CountryRanks (country TEXT PRIMARY KEY, rank INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineTable (country TEXT PRIMARY KEY, vaccinated INTEGER, percent NUMBER)")
    conn.commit()

def calculate_average_percent_vaccinated(cur):
    """Calculates the world average percent vaccinated"""
    cur.execute('SELECT percent FROM VaccineTable')
    percent_list = cur.fetchall()
    total_percent = 0
    num_countries = 0
    for p in percent_list:
        total_percent += p[0]
        num_countries += 1
    percent = (total_percent/num_countries)
    return round(percent, 2)

def sort_percentages(cur):
    """Sorts the countries by percent vaccinated and returns a list of tuples with the country name and percent vaccinated """
    cur.execute('SELECT country, percent FROM VaccineTable')
    countries = cur.fetchall()
    countries.sort(key = lambda x: x[1], reverse = True) 
    return countries

def write_data_file(filename, cur, conn):
    """Wrties the world average percent vaccinated and the top ten high vaccination percentages to a filename that is given in the input"""
    cur.execute('SELECT country FROM CountryRanks')
    countries = cur.fetchall()
    if len(countries) == 125:

        path = os.path.dirname(os.path.abspath(__file__)) + os.sep

        outFile = open(path + filename, "w")
        outFile.write("World Average Percent Vaccinated\n")
        outFile.write("=====================================================\n\n")
        percent = str(calculate_average_percent_vaccinated(cur))
        outFile.write(percent + "%" + "\n\n")
        outFile.write("Top Ten Highest Vaccination Percentages in the World\n")
        outFile.write("======================================================\n\n")
        country_list = sort_percentages(cur)
        outFile.write("1. " + str(country_list[0][0]) + "\n")
        outFile.write("2. " + str(country_list[1][0]) + "\n")
        outFile.write("3. " + str(country_list[2][0]) + "\n")
        outFile.write("4. " + str(country_list[3][0]) + "\n")
        outFile.write("5. " + str(country_list[4][0]) + "\n")
        outFile.write("6. " + str(country_list[5][0]) + "\n")
        outFile.write("7. " + str(country_list[6][0]) + "\n")
        outFile.write("8. " + str(country_list[7][0]) + "\n")
        outFile.write("9. " + str(country_list[8][0]) + "\n")
        outFile.write("10. " + str(country_list[9][0]) + "\n")
        outFile.close()

def main():
    """Calls the functions set_up_database(), set_up_vaccine_tables(), fill_country_rank_table(), fill_vaccine_table(), and write_data_file(). Closes the database connection. """
    cur, conn = set_up_database('vaccine.db')
    set_up_vaccine_tables(cur, conn)
    fill_country_rank_table(cur, conn)
    fill_vaccine_table(cur,conn)
    write_data_file("vaccine_data.txt", cur, conn)
    conn.close()


if __name__ == "__main__":
    main()