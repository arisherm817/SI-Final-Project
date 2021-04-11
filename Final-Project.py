import json
import unittest
import os
import requests

#The Effect of Covid-19 on Uber Times and Prices
#Team members: Lindsay Brenner and Ari Sherman 


def get_uber_prices():
    pass

def get_uber_time_estimates():
    pass

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
    
def get_month_covid_cases(month, year):
    month_cases = {}
    if month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10" or month == "12":
        month_cases = get_week_covid_cases("2021-{}-01".format(month), "2021-{}-08".format(month))
        month_cases.update(get_week_covid_cases("2021-{}-09".format(month), "2021-{}-16".format(month)))
        month_cases.update(get_week_covid_cases("2021-{}-17".format(month), "2021-{}-24".format(month)))
        month_cases.update(get_week_covid_cases("2021-{}-25".format(month), "2021-{}-31".format(month)))
    elif month == "02":
        if year % 4 == 0:
            month_cases = get_week_covid_cases("2021-{}-01".format(month), "2021-{}-08".format(month))
            month_cases.update(get_week_covid_cases("2021-{}-09".format(month), "2021-{}-16".format(month)))
            month_cases.update(get_week_covid_cases("2021-{}-17".format(month), "2021-{}-24".format(month)))
            month_cases.update(get_week_covid_cases("2021-{}-25".format(month), "2021-{}-29".format(month)))
        else :
            month_cases = get_week_covid_cases("2021-{}-01".format(month), "2021-{}-08".format(month))
            month_cases.update(get_week_covid_cases("2021-{}-09".format(month), "2021-{}-16".format(month)))
            month_cases.update(get_week_covid_cases("2021-{}-17".format(month), "2021-{}-24".format(month)))
            month_cases.update(get_week_covid_cases("2021-{}-25".format(month), "2021-{}-28".format(month)))
    else:
        month_cases = get_week_covid_cases("2021-{}-01".format(month), "2021-{}-08".format(month))
        month_cases.update(get_week_covid_cases("2021-{}-09".format(month), "2021-{}-16".format(month)))
        month_cases.update(get_week_covid_cases("2021-{}-17".format(month), "2021-{}-24".format(month)))
        month_cases.update(get_week_covid_cases("2021-{}-25".format(month), "2021-{}-30".format(month)))
    return month_cases


class TestFinalProject(unittest.TestCase):
    def test_get_uber_prices(self):
        
        pass

    def test_get_uber_time_estimates(self):
        
        pass

    def test_get_num_covid_cases(self):

        print(get_month_covid_cases("03"))
        

def main():


    print("-----Unittest-------")
    unittest.main(verbosity=2)
    print("------------")


if __name__ == "__main__":
    main()