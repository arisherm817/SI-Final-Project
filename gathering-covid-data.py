import json
import os
import requests
import sqlite3

#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 

def set_up_covid_table(cur, conn):
    """Pulls data from Covid API and sets up table with covid data """
    cur.execute("CREATE TABLE IF NOT EXISTS Covid (country TEXT PRIMARY KEY, confirmed INTEGER, deaths INTEGER, recovered INTEGER)")
    cur.execute('SELECT country FROM CountryRanks')
    countries = cur.fetchall()
    country_list = []
    for i in countries: 
        country_list.append(i[0])
    used_countries = []
    url = 'https://api.covid19api.com/summary'
    r = requests.get(url)
    data = r.text
    countries = json.loads(data)
    while len(used_countries) < 105: 
        count = 0 
        for country in countries['Countries']:
            if country['Country'] in used_countries: 
                continue
            else: 
                if country['Country'] in country_list or country['Country'] == 'United States of America': 
                    if country['Country'] == 'United States of America': 
                        c = 'United States'
                    else: 
                        c = country['Country']
                    confirmed = int(country['TotalConfirmed'])
                    deaths = int(country['TotalDeaths'])
                    recovered = int(country['TotalRecovered'])
                    cur.execute("INSERT OR IGNORE INTO Covid (country, confirmed, deaths, recovered) VALUES (?,?,?,?)", (c, confirmed, deaths, recovered))
                    count += 1
                    used_countries.append(country['Country'])
            if count == 25: 
                break
    conn.commit()
    
def calculate_death_rate(cur):
    """Uses information form Covid table to calculate the Covid death rate. Returns country names and death rates in descending order"""
    cur.execute('SELECT country, confirmed, deaths FROM Covid')
    tup = cur.fetchall()
    death_rate_list = []
    for country in tup: 
        if country[2] == 0: 
            continue 
        else: 
            death_rate = (country[2]/country[1])
            new = (country[0], round(death_rate, 3))
            death_rate_list.append(new)
    sorted_list = sorted(death_rate_list, key = lambda x: x[1], reverse = True)
    return sorted_list

def join_table(cur, conn):
    """Joins the Vaccine and Covid table. Returns a list of tuples with country names, total number vaccinated, and total number of confirmed cases """
    cur.execute("SELECT Covid.country, VaccineTable.vaccinated, Covid.confirmed FROM VaccineTable LEFT JOIN Covid ON VaccineTable.country = Covid.country") 
    results = cur.fetchall()
    conn.commit()
    return results

def calculate_cases_per_vaccine(cur, conn): 
    """Uses the joined table information to calculte the number of cases per vaccine in each country. Returns a list of tuples wiht the country name and the cases per vaccine"""
    results = join_table(cur, conn)
    cases_per_vaccine = {}
    for country in results: 
        if type(country[1]) != int or type(country[2]) != int or type(country[0]) != str: 
            continue
        else: 
            percent = (country[2] / country[1])
            cases_per_vaccine[country[0]] = round(percent, 3)
    sorted_dict = sorted(cases_per_vaccine.items(), key = lambda x: x[1])
    return sorted_dict


def write_data_file(filename, cur, conn):
    """Writes the top ten Covid-19 death rates per country anf the top ten fewest number of confirmed cases per vaccinated person to the filename given in the input """
    cur.execute('SELECT country FROM Covid')
    countries = cur.fetchall()
    if len(countries) >= 100:

        path = os.path.dirname(os.path.abspath(__file__)) + os.sep

        outFile = open(path + filename, "w")
        outFile.write("Top Ten COVID-19 Death Rates per Country\n")
        outFile.write("=====================================================\n\n")

        death_rate = calculate_death_rate(cur)
        count = 1
        for i in death_rate[:10]:  
            outFile.write(str(count) + '.  ' + str(i[0]) + "\n")
            count += 1
        outFile.write('\n\n')
       
        outFile.write("Top Ten Fewest Number of Confirmed Cases per Vaccinated Person per Country\n")
        outFile.write("======================================================\n\n")
        cases_per = calculate_cases_per_vaccine(cur, conn)
        count = 1
        for i in cases_per[:10]:  
            outFile.write(str(count) + '.  ' + str(i[0]) + "\n")
            count += 1
        outFile.close()
        
def main():
    """Calls the functions set_up_covid_table(), calculate_death_rate(), calculate_cases_per_vaccine(), write_data_file(). Closes connection to database"""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/vaccine.db')
    cur = conn.cursor()
    
    set_up_covid_table(cur, conn)
    calculate_death_rate(cur)
    calculate_cases_per_vaccine(cur, conn)
    write_data_file('covid_data.txt', cur, conn)
    conn.close()


if __name__ == "__main__":
    main()