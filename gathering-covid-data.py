import json
import os
import requests
import sqlite3

#Covid-19 Cases and Vaccines
#Team members: Lindsay Brenner and Ari Sherman 

def set_up_covid_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Covid (country_id INTEGER PRIMARY KEY, country TEXT, confirmed INTEGER, deaths INTEGER, recovered INTEGER)")
    cur.execute('SELECT country, country_id FROM CountryIds')
    countries = cur.fetchall()
    country_list = []
    country_id_list = []
    for i in countries: 
        country_list.append(i[0])
        country_id_list.append(i[1])
    used_countries = []
    url = 'https://api.covid19api.com/summary'
    r = requests.get(url)
    data = r.text
    countries = json.loads(data)
    country_string = ""
    for c in country_list:
        country_string += c + ' '
    while len(used_countries) < 125: 
        count = 0 
        for country in countries['Countries']:
            if country['Country'] in used_countries: 
                continue
            else: 
                if country['Country'] in country_string: 
                    confirmed = int(country['TotalConfirmed'])
                    deaths = int(country['TotalDeaths'])
                    recovered = int(country['TotalRecovered'])
                    countryid = country_id_list[country_list.index(country['Country'])]
                    cur.execute("INSERT OR IGNORE INTO Covid (country_id, country, confirmed, deaths, recovered) VALUES (?,?,?,?,?)", (countryid, country['Country'], confirmed, deaths, recovered))
                    count += 1
                    used_countries.append(country['Country'])
            if count == 25: 
                break
    conn.commit()
    

def join_table(cur, conn):
    pass 
    
def write_data_file(filename, cur, conn):
    pass
        
def main():
    """Takes no inputs and returns nothing."""
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path + '/vaccine.db')
    cur = conn.cursor()
    
    set_up_covid_table(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()