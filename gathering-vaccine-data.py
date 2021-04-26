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

def get_vaccine_number_data():
    """Returns a dictionary with the key being the name of the country and the value being a tuple in the format (Percent Vaccinated, Total Vaccinations). """
    """Uses BeautifulSoup to read the countries name, the countries percent vaccinated, and total vaccinations"""
    nums = []
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
        number = (tds[1].text.replace(',', ''))
        if country == "EU":
            continue
        else:
            nums.append((country, int(number)))
    sorted_data = sorted(nums, key = lambda x: x[1], reverse = True)
    return sorted_data

def get_vaccine_percent_data():
        percents = []
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
            percent = tds[2].text.strip('%')
            if percent == '--' or country == "EU" or float(percent) == 0 or float(percent) > 100:
                continue
            else:
                percents.append((country, float(percent)))
        sorted_data = sorted(percents, key = lambda x: x[1], reverse = True)
        return sorted_data
    

def fill_vaccine_number_table(cur, conn): 
    """ Fills the Vaccine Table table with the country names, the total number of vaccinations in the country, and the percent of the country population that is vaccinated"""
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineNumberTable (country_id TEXT PRIMARY KEY, country TEXT, vaccinated INTEGER)")
    countries = get_vaccine_number_data()

    cur.execute("SELECT MAX(country_id) FROM VaccineNumberTable")
    max_id = cur.fetchone()[0]
    num_entries = 25
    if (type(max_id) != int):
        id_num = 0
    elif (len(countries) - max_id) < 25:
        id_num = int(max_id)
        num_entries = len(countries) - max_id
    else:
        id_num = int(max_id)
    
    for country in countries[id_num:id_num + num_entries]:
        cur.execute("INSERT OR IGNORE INTO VaccineNumberTable (country_id, country, vaccinated) VALUES (?,?,?)", (id_num+1, country[0], country[1]))
        id_num += 1
        
    conn.commit()

def fill_vaccine_percent_table(cur, conn): 
    """ Fills the Vaccine Table table with the country names, the total number of vaccinations in the country, and the percent of the country population that is vaccinated"""
    cur.execute("CREATE TABLE IF NOT EXISTS VaccinePercentTable (country_id TEXT PRIMARY KEY, percent NUMBER)")
    countries = get_vaccine_percent_data()
    count = 0
    
    for i in range(167):
        statement = "SELECT country_id FROM VaccineNumberTable WHERE country = '{}'".format(countries[i][0])
        cur.execute(statement)
        id_num = cur.fetchone()[0]
        statement1 = "SELECT percent FROM VaccinePercentTable WHERE country_id = {}".format(id_num)
        cur.execute(statement1)
        j = cur.fetchone()
        if j == None:
            cur.execute("INSERT OR IGNORE INTO VaccinePercentTable (country_id, percent) VALUES (?,?)", (id_num, countries[i][1]))
            count += 1
        if count == 25:
            break
        
    conn.commit()


def set_up_vaccine_table(cur, conn):
    """Creates two tables. One table that contain the country vaccination rankings and another table that has vaccine data for each country """
    cur.execute("CREATE TABLE IF NOT EXISTS VaccinePercentTable (country_id INTEGER PRIMARY KEY, percent NUMBER)")
    cur.execute("CREATE TABLE IF NOT EXISTS VaccineNumberTable (country_id INTEGER PRIMARY KEY, country TEXT, vaccinated INTEGER)")
    conn.commit()

def calculate_average_percent_vaccinated(cur):
    """Calculates the world average percent vaccinated"""
    cur.execute('SELECT percent FROM VaccinePercentTable')
    percent_list = cur.fetchall()
    total_percent = 0
    num_countries = 0
    for p in percent_list:
        total_percent += p[0]
        num_countries += 1
    percent = (total_percent/num_countries)
    return round(percent, 2)

def top_ten_percentages(cur):
    """Sorts the countries by percent vaccinated and returns a list of tuples with the country name and percent vaccinated """
    cur.execute('SELECT country_id, percent FROM VaccinePercentTable')
    countries = cur.fetchall()
    countries.sort(key = lambda x: x[1], reverse = True) 
    return countries[:10]

def write_data_file(filename, cur, conn):
    """Wrties the world average percent vaccinated and the top ten high vaccination percentages to a filename that is given in the input"""
    cur.execute('SELECT country_id FROM VaccinePercentTable')
    num_countries = len(cur.fetchall())
    if num_countries == 167:

        path = os.path.dirname(os.path.abspath(__file__)) + os.sep

        outFile = open(path + filename, "w")
        outFile.write("World Average Percent Vaccinated\n")
        outFile.write("=====================================================\n\n")
        percent = str(calculate_average_percent_vaccinated(cur))
        outFile.write(percent + "%" + "\n\n")
        outFile.write("Top Ten Highest Vaccination Percentages in the World\n")
        outFile.write("======================================================\n\n")
        country_list = top_ten_percentages(cur)
        count = 1
        for country in country_list:
            statement = "SELECT country FROM VaccineNumberTable WHERE country_id = {}".format(country[0])
            cur.execute(statement)
            country1 = cur.fetchone()[0]
            outFile.write(str(count) + ". " + str(country1) + " has about " + str(country[1]) + "% of its population vaccinated\n")
            count += 1
        outFile.close()

def main():
    """Calls the functions set_up_database(), set_up_vaccine_tables(), fill_vaccine_table(), and write_data_file(). Closes the database connection. """
    cur, conn = set_up_database('vaccine.db')
    set_up_vaccine_table(cur, conn)
    fill_vaccine_number_table(cur,conn)
    cur.execute("SELECT MAX(country_id) FROM VaccineNumberTable")
    max_id = cur.fetchone()[0]
    if (max_id == 190):
        fill_vaccine_percent_table(cur,conn)
    write_data_file("vaccine_data.txt", cur, conn)
    conn.close()


if __name__ == "__main__":
    main()