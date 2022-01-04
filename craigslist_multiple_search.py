import requests
import time
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Firefox()

# URL that region's and subregion's names and URLs are scraped from, used to get list of search areas and corresponding URLs
url_craigslist_region_webpage = 'https://www.craigslist.org/about/sites#US'


# check if page loads
downloaded_webpage_craigslist_regions = requests.get(url_craigslist_region_webpage)

if downloaded_webpage_craigslist_regions.status_code == requests.codes.ok or downloaded_webpage_craigslist_regions.status_code == requests.codes.ok:
    True

else:
    print(str(url_craigslist_region_webpage) + ' webpage did not load!!!!')


# open webpage
driver.get(url_craigslist_region_webpage)


# create list of regions
element_list_regions = driver.find_elements(By.CSS_SELECTOR, 'div.colmask > div > h4')

region_list = []
for region in element_list_regions:
    region_list.append(region.text)


# create list of subregion urls
element_list_subregion_urls = driver.find_elements(By.CSS_SELECTOR,'div.colmask > div > ul > li > a' )


subregion__url_list = []
for url in element_list_subregion_urls:
    subregion__url_list.append(url.get_attribute('href'))


# create list of region and subregion names (region names start with an uppercase letter, subregions start with a lowercase)
element_list_region_and_subregions = driver.find_elements(By.CSS_SELECTOR,'div.colmask')

list_region_and_subregions_list = []
for elem in element_list_region_and_subregions:
    list_region_and_subregions_list.append(elem.text.splitlines())

region_and_subregions_list = []
for list in list_region_and_subregions_list:
    for string in list:
        region_and_subregions_list.append(string)


# create region and subregion url list
region_and_subregion_url_list = []
x = 0
for region_or_subregion in region_and_subregions_list:
    if region_or_subregion in region_list:
        region_and_subregion_url_list.append(region_or_subregion)
    else:
        region_and_subregion_url_list.append(subregion__url_list[x])
        x += 1


## create url list based on user input of which states to search

url_list_revised = []

# get user input list of states to search
state_input_list = [str(x) for x in input('Enter the states to search (separate by commas): ').split(',')]


for state_input in state_input_list:

    state_input = state_input.strip()

    if state_input[0].isupper() == False:
        state_input = state_input.capitalize()

    index = region_and_subregions_list.index(state_input)


    # create url list with all subregion urls for states

    url_list = []

    region_or_url_string = region_and_subregion_url_list[index+1]

    x = 1


    while region_or_url_string[0].isupper() == False:
        url_list.append(region_or_url_string)
        x+=1
        region_or_url_string = region_and_subregion_url_list[index+x]


    # create subregion list for states

    subregion_list = []

    region_or_subregion_string = region_and_subregions_list[index+1]   

    y = 1

    while region_or_subregion_string[0].isupper() == False:
        subregion_list.append(region_or_subregion_string)
        y+=1
        region_or_subregion_string = region_and_subregions_list[index+y]


    # show user subregions

    print(state_input + ' subregions to search:')
    n = 1
    for subregion in subregion_list:
        print(str(n) + ': ' + str(subregion))
        n += 1

    # get input from user on which regions to search and update url list per input

    search_number_list = [int(x) for x in input('Enter the corresponding numbers of the subregions to search (separate input numbers by spaces): ').split()]

    for number in search_number_list:
        url_list_revised.append(url_list[number-1])

url_list = url_list_revised


## Get user input search parameters

input_search_keyword = input('Enter Search Keyword: ')
input_min_price = input('Enter Minimum Price: ')
input_max_price = input('Enter Maximum Price: ')

window_index = 1

for url in url_list:

    time.sleep(0.1)

    downloaded_webpage = requests.get(url)

    # check if page loads
    if downloaded_webpage.status_code == requests.codes.ok or downloaded_webpage.status_code == requests.codes.ok:
        True

    else:
        print(str(url) + ' webpage did not load!!!!')
        continue

    # input search keywords into search bar

     # open new tab
    driver.execute_script('window.open('');')

    driver.switch_to.window(driver.window_handles[window_index])
    window_index += 1

    driver.get(url)

    # input search parameters

    for_sale = driver.find_element(By.XPATH,'/html/body/div/section/div[4]/div[2]/div[2]/h3/a/span')

    for_sale.click()

    min_price = driver.find_element(By.XPATH, '/html/body/section/form/div[2]/div[2]/div[5]/input[1]')

    max_price = driver.find_element(By.XPATH, '/html/body/section/form/div[2]/div[2]/div[5]/input[2]')


    min_price.send_keys(input_min_price)

    max_price.send_keys(input_max_price)

    search = driver.find_element(By.XPATH, '//*[@id="query"]')

    search.send_keys(input_search_keyword)
    
    search.submit()

    time.sleep(0.1)


