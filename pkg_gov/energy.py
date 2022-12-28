from bs4 import BeautifulSoup  ## BeautifulSoup is a web parsing package to help pull specific HTML components
import pandas as pd 
from datetime import date, timedelta
import requests 

def energy_scrape():
    ## Date List created with string values for the last 4 days to only pull opinions from that range.  
    ## General templates to pull from, not all are always used.
    today = date.today()
    yesterday = date.today() - timedelta(1)
    two_ago = date.today() - timedelta(2)
    today_word = today.strftime("%B %d, %Y")
    today_word_single_digit_day = today.strftime("%B %d, %Y").replace(" 0", " ")
    yesterday_word = yesterday.strftime("%B %d, %Y")
    yesterday_word_single_digit_day = yesterday.strftime("%B %d, %Y").replace(" 0", " ")
    two_ago_word = two_ago.strftime("%B %d, %Y")
    two_ago_word_single_digit_day = two_ago.strftime("%B %d, %Y").replace(" 0", " ")
    date_list = [today_word,yesterday_word,two_ago_word,today_word_single_digit_day,yesterday_word_single_digit_day,two_ago_word_single_digit_day]

    ## Headers is used because a User-Agent was required by the website
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'}
    link = "https://www.energy.gov/listings/energy-news"

    ##** Error Handling for bad URL
    try:
        page = requests.get(link, headers=headers)
        page.raise_for_status()
    except:
        print('URL Broken')
        obj_list = [{'type':'Government','source':'Energy Dept', 'title': 'Link Broken', 'link': '', 'Notes': '', 'date': ''}]
        energy_dept_df = pd.DataFrame(obj_list)
        return energy_dept_df
        
    ## Parse the webpage
    page = requests.get(link, headers=headers)
    soup = BeautifulSoup(page.content, 'lxml')

    ## Actual HTML pull
    object_list = []
    for item in soup.find_all(class_='search-result'):

        if item.find(class_='search-result-display-date').get_text() in date_list:

            title = item.find(class_='search-result-title').get_text()
            ilink = "https://www.energy.gov" + item.find(class_='search-result-title').get('href')
            notes = item.find(class_='search-result-summary').get_text()
            idate = item.find(class_='search-result-display-date').get_text()
            obj_data = {'type':'Government','source':'Energy Dept', 'title': title, 'link': ilink, 'Notes': notes, 'date': idate}
            object_list.append(obj_data)

    if len(object_list) == 0:
        item = soup.find(class_='search-result')
        title = item.find(class_='search-result-title').get_text()
        ilink = "https://www.energy.gov" + item.find(class_='search-result-title').get('href')
        notes = item.find(class_='search-result-summary').get_text()
        idate = item.find(class_='search-result-display-date').get_text()
        obj_data = {'type':'Government','source':'Energy Dept', 'title': title, 'link': ilink, 'Notes': 'Query Working, No New Posts', 'date': idate}
        object_list.append(obj_data)

    ## Final dataframe is defined
    energy_dept_df = pd.DataFrame(object_list)

    ##** Error Handling for empty result
    if len(energy_dept_df) == 0:
        print('No Result')
        obj_list = [{'type':'Government','source':'Energy Dept', 'title': 'Tags Not Found', 'link': '', 'Notes': '', 'date': ''}]
        energy_dept_df = pd.DataFrame(obj_list)
        return energy_dept_df

    print(energy_dept_df)
    return energy_dept_df
    
energy_scrape()
