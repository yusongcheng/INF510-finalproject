import requests
from bs4 import BeautifulSoup
import pandas as pd

def retrieve_url(url):
    try:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'lxml')
        r.close()
        return soup
    except:
        return 'wrong url'

def get_url_for_each_location(soup: BeautifulSoup):
    restaurants_by_location_list = []
    for restaurants in soup.findAll('h3', attrs={'class': 'lght'}):
        res_url = restaurants.find('a').attrs['href']
        restaurants_by_location_list.append(res_url)
    return restaurants_by_location_list

#for counting the stars for each restaurant in LA
def count_star(soup: BeautifulSoup):
    full_star = soup.findAll('i', attrs={'class' : 'fa fa-star'})
    half_star = soup.findAll('i', attrs={'class' : 'fa fa-star-half-o'})
    return len(full_star)+len(half_star)/2

#try next page
def try_next(url):
    try:
        soup = retrieve_url(url)
        soup.findAll('li', attrs={'class': 'page-item'})[2]
        return True
    except:
        return False

#find information for each restaurant based on soup object
#return a list of info about all restaurants of the same page
def find_one_page_info(url):
    soup = retrieve_url(url)
    restaurant_list = []
    for each_res in soup.findAll('div', attrs={'class': 'shadow-div p-4'}):
        # get name
        restaurant_name = each_res.find('a').find('span').get_text()
        # get address locality and zipcode
        temp = each_res.find('address')
        restaurant_streetaddress = temp.find('span', attrs={'itemprop': 'streetAddress'}).get_text()
        restaurant_locality = temp.find('span', attrs={'itemprop': 'addressLocality'}).get_text()
        restaurant_zipcode = temp.find('span', attrs={'itemprop': 'postalCode'}).get_text()
        # get price level
        restaurant_price = each_res.find('div', attrs={'class': 'mb-2'}).find('span').get_text()
        # get star
        restaurant_stars = count_star(each_res)
        restaurant_list.append([restaurant_name, restaurant_streetaddress, restaurant_locality, restaurant_zipcode, restaurant_price, restaurant_stars])
    return restaurant_list

#once we get url for each location, use this function to get each restaurant info through each url if there is a 'next page'
def find_info_for_all_pages(url):
    prefix = url
    restaurant_info_list = find_one_page_info(url)
    page_text = '?page='
    page = 2
    while True:
        if try_next(url) == True:
            url = prefix + page_text + str(page)
            restaurant_info_list += find_one_page_info(url)
            page += 1
        else:
            break
    return restaurant_info_list

def transfer_list_into_pandas(restaurant_list):
    restaurant_info = {'res_name': [], 'res_streetaddress': [], 'res_locality': [], 'zipcode': [], 'res_price': [], 'res_stars': []}
    for each_res_info in restaurant_list:
        restaurant_info['res_name'].append(each_res_info[0])
        restaurant_info['res_streetaddress'].append(each_res_info[1])
        restaurant_info['res_locality'].append(each_res_info[2])
        restaurant_info['zipcode'].append(each_res_info[3])
        restaurant_info['res_price'].append(each_res_info[4])
        restaurant_info['res_stars'].append(each_res_info[5])
    restaurant_info_df = pd.DataFrame(restaurant_info)
    return restaurant_info_df

def parse_restaurant_info_data_set_la():
    restaurant_info_list = []

    table_agent_url = 'https://tableagent.com/los-angeles/location/'
    url_prefix = 'http://tableagent.com'
    url_list = get_url_for_each_location(retrieve_url(table_agent_url))
    #go to each url of many restaurants in the same location
    for url_suffix in url_list:
        url = url_prefix + url_suffix
        restaurant_info_list += find_info_for_all_pages(url)
    restaurant_info_df = transfer_list_into_pandas(restaurant_info_list)
    return restaurant_info_df



