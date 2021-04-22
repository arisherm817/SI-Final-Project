import json
import requests
import sqlite3
import unittest
import os

#The Effect of Covid-19 on Uber Times and Prices
#Team members: Lindsay Brenner and Ari Sherman 



def get_week_covid_cases(start_date, end_date):
    cases_dict = {}
    url = 'https://api.covid19api.com/country/united-states/status/confirmed?from={}T00:00:00Z&to={}T00:00:00Z'
    request_url = url.format(start_date, end_date)
    r = requests.get(request_url)
    data = r.text
    days = json.loads(data)
    for day in days:
        date = day['Date'].split('T')
        cases_dict[date[0]] = int(day['Cases'])
    return cases_dict
    
def get_month_covid_cases(year, month):
    month_cases = {}
    if month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12":
        month_cases = get_week_covid_cases("{}-{}-01".format(year, month), "{}-{}-08".format(year, month))
        month_cases.update(get_week_covid_cases("{}-{}-09".format(year, month), "{}-{}-16".format(year, month)))
        month_cases.update(get_week_covid_cases("{}-{}-17".format(year, month), "{}-{}-24".format(year, month)))
        month_cases.update(get_week_covid_cases("{}-{}-25".format(year, month), "{}-{}-31".format(year, month)))
    elif month == "02":
        if int(year) % 4 == 0:
            month_cases = get_week_covid_cases("{}-{}-01".format(year, month), "{}-{}-08".format(year, month))
            month_cases.update(get_week_covid_cases("{}-{}-09".format(year, month), "{}-{}-16".format(year, month)))
            month_cases.update(get_week_covid_cases("{}-{}-17".format(year, month), "{}-{}-24".format(year, month)))
            month_cases.update(get_week_covid_cases("{}-{}-25".format(year, month), "{}-{}-29".format(year, month)))
        else :
            month_cases = get_week_covid_cases("{}-{}-01".format(year, month), "{}-{}-08".format(year, month))
            month_cases.update(get_week_covid_cases("{}-{}-09".format(year, month), "{}-{}-16".format(year, month)))
            month_cases.update(get_week_covid_cases("{}-{}-17".format(year, month), "{}-{}-24".format(year, month)))
            month_cases.update(get_week_covid_cases("{}-{}-25".format(year, month), "{}-{}-28".format(year, month)))
    else:
        month_cases = get_week_covid_cases("{}-{}-01".format(year, month), "{}-{}-08".format(year, month))
        month_cases.update(get_week_covid_cases("{}-{}-09".format(year, month), "{}-{}-16".format(year, month)))
        month_cases.update(get_week_covid_cases("{}-{}-17".format(year, month), "{}-{}-24".format(year, month)))
        month_cases.update(get_week_covid_cases("{}-{}-25".format(year, month), "{}-{}-30".format(year, month)))
    return month_cases


class TestFinalProject(unittest.TestCase):
    

    def test_get_num_covid_cases(self):
        # print(get_month_covid_cases('2020', '02'))
        # print(get_month_covid_cases('2021', '02'))
        pass

def main():
    print("-----Unittest-------")
    unittest.main(verbosity=2)
    print("------------")


if __name__ == "__main__":
    main()