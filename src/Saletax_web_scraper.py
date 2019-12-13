import requests
import pandas as pd
from bs4 import BeautifulSoup

def retrieve_url(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        r.close()
        return soup
    except:
        return 'wrong url'

def get_tax_from_final_url(url):
    soup = retrieve_url(url)
    tax_list = []
    tax_rate = soup.find('span', attrs={'class' : 'fixe'}).find('select').findAll('option')
    for eachtax in tax_rate:
        tax_list.append(eachtax.get_text())
    return tax_list

def get_zip_finalsuffix_from_city_url(url):
    zip_suffix_list = []
    soup = retrieve_url(url)
    zipthings = soup.find('ul', attrs={'class': 'active'}).findAll('li')
    for each in zipthings:
        zipcode = each.find('a').get_text()
        suffix = each.find('a').attrs['href']
        zip_suffix_list.append([zipcode, suffix])
    return zip_suffix_list


def get_zip_tax():
    url = 'http://www.salestaxstates.com/sales-tax-calculator-california'
    city_suffix_list = []
    zipcode_finalsuffix_list = []
    zipcode_tax_info = {'zipcode':[], 'tax':[]}
    prefix = 'http://www.salestaxstates.com/'
    soup = retrieve_url(url)
    city_in_CA = soup.find('ul', attrs={'class' : 'hide allCities'}).findAll('li')
    for each in city_in_CA:
        city_suffix_list.append(each.find('a').attrs['href'])#add suffix for each city

    for suffix in city_suffix_list:
        url = prefix + suffix
        zipcode_finalsuffix_list += get_zip_finalsuffix_from_city_url(url)

    for zipcode_finalsuffix in zipcode_finalsuffix_list:
        zipcode = zipcode_finalsuffix[0]
        finalsuffix = zipcode_finalsuffix[1]
        url = prefix + finalsuffix
        tax_rate = get_tax_from_final_url(url)
        zipcode_tax_info['zipcode'].append(zipcode)
        zipcode_tax_info['tax'].append(tax_rate)
    zipcode_tax_info_df = pd.DataFrame(zipcode_tax_info)
    return zipcode_tax_info_df




