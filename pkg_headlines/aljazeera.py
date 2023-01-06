from bs4 import BeautifulSoup  ## BeautifulSoup is a web parsing package to help pull specific HTML components
import urllib.request  ## to get a access to a URL and its content
import pandas as pd 
from datetime import date, timedelta, datetime
import requests 

## Date List created with string values for the last 4 days to only pull opinions from that range.  
## General templates to pull from, not all are always used.
today = date.today()
yesterday = date.today() - timedelta(1)
today_word = today.strftime("%B %d, %Y")
yesterday_word = yesterday.strftime("%B %d, %Y")
today_link = today.strftime("%Y/%m/%d/")
date_list = [today_word,yesterday_word]

## Headers is used because a User-Agemt was required by the website
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 Edg/90.0.818.46'}
link = "https://www.aljazeera.com/search/the"

##** Error Handling for bad URL
try:
    page = requests.get(link, headers=headers)
    page.raise_for_status()
except:
    print('URL Broken')
    obj_list = [{'type':'Headline','source':'AlJazeera', 'title': 'Link Broken', 'link': '', 'Notes': '', 'date': ''}]
    aljazeera_df = pd.DataFrame(obj_list)
    
## Parse the webpage
page = requests.get(link, headers=headers)
soup = BeautifulSoup(page.content, 'lxml')

## Actual HTML pull
object_list = []
for item in soup.find_all(class_='gc__content')[:10]:
    #if item.find('span').get_text() in date_list:
    title = item.find('span').get_text()
    ilink = item.find('a').get('href')  
    notes = item.find(class_='gc__excerpt').find('p').get_text()
    idate = item.find(class_='screen-reader-text').get_text().lstrip('Published On')

    obj_data = {'type':'Headline','source':'AlJazeera', 'title': title, 'link': ilink, 'Notes': notes, 'date': idate}
    object_list.append(obj_data)

## Final dataframe is defined
aljazeera_df = pd.DataFrame(object_list)

    ##** Error Handling for empty result
if len(aljazeera_df) == 0:
    print('No Results')
    obj_list = [{'type':'Headline','source':'AlJazeera', 'title': 'Data List Empty', 'link': '', 'Notes': '', 'date': ''}]
    aljazeera_df = pd.DataFrame(obj_list)
## Final Return Statement
print(aljazeera_df)
