# to run this in the django shell type the line below in the command line
# python manage.py shell < db.py


import webbrowser
import requests
import time
import bs4
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import shutil
from urllib. request import urlopen

# create dictionary and list
accident_dictionary = {}


# define which accident webpages to run

#x = 794

for j in range(1, 796, 1):

    time.sleep(1)


    # define url of webpage to scrape
    url_inv =  f'https://avalanche.state.co.us/caic/acc/acc_report.php?acc_id={j}&accfm=inv'

    url_rep =  f'https://avalanche.state.co.us/caic/acc/acc_report.php?acc_id={j}&accfm=rep'


    downloaded_webpage_ending_with_inv = requests.get(url_inv)
    downloaded_webpage_ending_with_rep = requests.get(url_rep)

    # check if page loads
    if downloaded_webpage_ending_with_inv.status_code == requests.codes.ok or downloaded_webpage_ending_with_rep.status_code == requests.codes.ok:
        True

    else:
        print('key: ' + str(j) + ' webpage did not load!!!!')
        continue


    # function that takes a url and element and returns a list of strings

    def element_to_list(url, element):

        downloaded_webpage = requests.get(url)

        soup_object = BeautifulSoup(downloaded_webpage.content, 'html.parser')
    
        element = soup_object.select(element)

        element_list = []

        for i in range(len(element)):
            element_list.append(element[i].getText())

        return element_list


    url = url_inv

    string_list_element_ul = element_to_list(url, 'ul')

    # check if url_inv is empty, and use url_rep if it is
    if string_list_element_ul[0][11] == '-':
        url = url_rep
        string_list_element_ul = element_to_list(url, 'ul')

    else: 
        True


    string_list_split = [(item.split('\n')) for item in string_list_element_ul]


    string_list_cleaned = []

    for list in string_list_split:
        for string in list:
            string = string.replace('xa0', ' ')
            string = string.replace('\xa0', ' ')
            string_list_cleaned.append(string)


    target_string_list = ['Location:', 'State:', 'Date:', 'Summary Description:', 'Primary Activity:', 'Primary Travel Mode:', 'Location Setting:', 'Killed:', 'Type:']
    

    strings_in_target_and_cleaned_lists = []


    for target_string in target_string_list:
        for string_cleaned in string_list_cleaned:
            if target_string in string_cleaned:
                strings_in_target_and_cleaned_lists.append(string_cleaned)

    
    for i in range(len(target_string_list)):
        if len(strings_in_target_and_cleaned_lists[i]) < 1:
            strings_in_target_and_cleaned_lists.insert(i, str(target_string_list[i]) + ' No Data')
        elif target_string_list[i][0] != strings_in_target_and_cleaned_lists[i][0]:
            strings_in_target_and_cleaned_lists.insert(i, str(target_string_list[i]) + ' No Data')
        else:
            continue


    accident_data_list = []


    for string in strings_in_target_and_cleaned_lists:
        string_split = string.split(':')
        accident_data_list.append(string_split[1].strip(' '))


    for i in range(len(accident_data_list)):
        if accident_data_list[i] == '' or accident_data_list[i] == '--':
            accident_data_list[i] = 'No Data'


    if accident_data_list[7] == 'No Data':
        accident_data_list[7] = int(0)


    # if number of people killed is greater than 0
    if int(accident_data_list[7]) > 0:
            # add accident_data_list and url to the accident dictionary
            accident_dictionary[j] = accident_data_list
            accident_dictionary[j].insert(0, url)

            # get html string
            html = urlopen(url).read()
            html_string = BeautifulSoup(html, 'lxml')


            # create html file of the CAIC accident webpage
            #html_file_accident_webpage = requests.get(url)
            
            #html_file_accident_webpage.raise_for_status()

            # creates new file in 'write binary' mode
            #open_html_file_accident_webpage = open(f'accident_html_{j}.html', 'wb')

            # Loops through text and writes text file every 100000 bytes
            #for chunk in html_file_accident_webpage.iter_content(100000):
                #open_html_file_accident_webpage.write(chunk)

            # close the file
            #open_html_file_accident_webpage.close()


            #text_html_file = open(f'accident_html_{j}.html')

            #text_html_soup_object = bs4.BeautifulSoup(text_html_file.read(), features='lxml')


            #entire_webpage_string = text_html_soup_object.get_text()

            #entire_webpage_string_split_at_AvalancheDetails = entire_webpage_string.split('Avalanche Details')

            #item_1_of_entire_webpage_string_split_at_Media = entire_webpage_string_split_at_AvalancheDetails[1].split('Media')

            #accident_summary_text_for_audio_file = item_1_of_entire_webpage_string_split_at_Media[0]

            #accident_summary_text_for_audio_file_split = accident_summary_text_for_audio_file.split('\n')

            #list_of_text_lines = []

            #for string in accident_summary_text_for_audio_file_split:
                #if string != '\n' and string != '' and string != ' ':
                    #list_of_text_lines.append(string)


            #text_cleaned = '\n'.join(list_of_text_lines)


            # write .txt file using text string

            #with open(f'accident_text_{j}.txt', 'w') as accident_text:
                #accident_text.write(text_cleaned)


            # use pico2wave to create audio file from text file
            #os.system(f'pico2wave -w accident_audio_{j}.wav "$(cat accident_text_{j}.txt)"')


# get lat and long
driver = webdriver.Firefox()

for key in accident_dictionary:

    # clean up location string and separate string into a list of words
    location = str(accident_dictionary[key][1])

    location_word_list = location.split(' ')
    
    for i in range(len(location_word_list)):
        location_word_list[i] = location_word_list[i].translate({ord(character): None for character in '/,.-'})


    # remove words that confuse google/maps

    remove_word_list = ['', 'Near', 'near', 'OB', 'in', 'bounds', 'off', 'trail', 'but', 'of', 'north', 'east', 'south', 'west', 'Town', 'of', 'outside', 'northern', 'southern', 'eastern', 'western', 'Drainage', 'drainage', 'The', 'Ballroom', 'side', 'West', 'East', 'North', 'South', 'zone', 'Zone', 'back', 'country', 'Backcountry', 'backcountry', 'to', 'the', 'To', 'northwestern', 'northern', 'northeastern', 'eastern', 'southeastern', 'southern', 'southwestern', 'western', 'NW', 'N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'Temptation', 'Avalanche', 'avalanche', 'path', 'Path', 'northwest', 'northeast', 'southeast', 'southwest', 'Northwest', 'Northeast', 'Southwest', 'Southeast', 'Bozeman', 'Steep', 'Gully', 'steep', 'gully', '#1', 'Peak', 'peak', '6996', '-', 'beavers', 'Shields', 'miles', '20']

    for word in remove_word_list:
        [location_word_list.remove(word) for word in location_word_list if word in remove_word_list]
  
    # create string of location description with list of remaining words
    location_string = ''

    for word in location_word_list:
        if word == 'A':
            word = 'Arapahoe'
        if word == '6996False':
            word = 'Peak 6996'
        location_string += str(word) + '+'
    
    print(location_word_list)


    ###  Scrape url from each webpage so lat/long can be extracted from url

    # define URL of webpage to scrape
    google_maps_search_url =  'http://www.google.com/maps/search/' + location_string + str(accident_dictionary[key][2])

    print(google_maps_search_url)

    driver.get(google_maps_search_url)

    # make sure page is fully loaded (probably a better way to do this)
    web_address_with_latlong = driver.current_url

    while '@' not in web_address_with_latlong:
        time.sleep(0.05)
        web_address_with_latlong = driver.current_url
  
    
    url_split_at = web_address_with_latlong.split('@')

    url_split_comma = url_split_at[1].split(',')


    lat = url_split_comma[0]

    long = url_split_comma[1]


    accident_dictionary.get(key).append(lat)

    accident_dictionary.get(key).append(long)


    accident_dictionary[key].append(str(html_string))


    print(key)
    print('\n')

# structure of dictionary: {key: [url, Location, State, Date, Summary Description, Primary Activity, Primary Travel Mode, Location Setting, Killed, Type, Lat, Long]}

# add data to django sql database

from django.utils import timezone
from podcast_data.models import Avalanche_Accident

# delete all rows in database
Avalanche_Accident.objects.all().delete()

for key in accident_dictionary:
    print(f'sql {key}')

    a = Avalanche_Accident(avalanche_number = key, url = accident_dictionary[key][0], location = accident_dictionary[key][1], state = accident_dictionary[key][2], date = accident_dictionary[key][3], summary_description = accident_dictionary[key][4], primary_activity = accident_dictionary[key][5], primary_travel_mode = accident_dictionary[key][6], location_setting = accident_dictionary[key][7], killed = accident_dictionary[key][8], type = accident_dictionary[key][9], latitude = accident_dictionary[key][10], longitude = accident_dictionary[key][11], html = accident_dictionary[key][12], pub_date = timezone.now())

    #a = Avalanche_Accident(avalanche_number = key, url = accident_dictionary[key][0], pub_date = timezone.now())

    a.save()
