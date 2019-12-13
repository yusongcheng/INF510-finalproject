import Tableagent_web_scraper as res
import Saletax_web_scraper as tax
import Openweather_api_crawler as weather
import pandas as pd
import argparse

'''get three dataframes (restaurant_info, tax_info, weather_info)'''
def grab_data_by_scraping_and_api_requests():

    #get a table of restarants information from Tableagent website
    '''https://tableagent.com/los-angeles/location/'''
    restaurant_info = res.parse_restaurant_info_data_set_la()

    #get a table of sale tax by zipcode from saletax website
    '''http://www.salestaxstates.com/sales-tax-calculator-california-los_angeles'''
    tax_info = tax.get_zip_tax()

    #get current weather information through api from Openweather website
    '''ducmentation: https://openweathermap.org/api'''
    zip_list = []
    for each in restaurant_info['zipcode']:
        zip_list.append(each)
    zip_list = list(set(zip_list))
    weather_info = weather.get_zipcode_weather(zip_list)
    return [restaurant_info,tax_info,weather_info]

'''get data from local csv files'''
def grab_data_from_downloaded_raw_files():
    restaurant_info = pd.read_csv('data/raw_restaurant_info.csv')
    tax_info = pd.read_csv('data/raw_tax_info.csv')
    weather_info = pd.read_csv('data/raw_weather_info.csv')
    return [restaurant_info,tax_info,weather_info]

def process_data(data):
     restaurant_info = data[0]
     price_temp = []
     for each in restaurant_info['res_price']:
         count = 0
         for i in each:
             if i == '$':
                 count += 1
         price_temp.append(count)
     restaurant_info['res_price']=price_temp

     tax_info = data[1]

     weather_info = data[2]
     return [restaurant_info, tax_info, weather_info]

def add_data_to_my_data_model(clean_data):
    '''save these data as csv files'''
    clean_data[0].to_csv("data/restaurant_info.csv", index=False, sep=',')
    clean_data[1].to_csv("data/tax_info.csv", index=False, sep=',')
    clean_data[2].to_csv("data/weather_info.csv", index=False, sep=',')
    print('Successfully! data have been already stored as csv files in the data sub folder')
    print('There shall be three files totally')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-source", choices=["local", "remote"], help="where data should be gotten from")
    args = parser.parse_args()

    location = args.source

    if location == "local":
        data = grab_data_from_downloaded_raw_files()
    else:
        print('please wait for several minutes to grab the data')
        data = grab_data_by_scraping_and_api_requests()

    data = process_data(data)
    add_data_to_my_data_model(data)

if __name__ == '__main__':
    main()



