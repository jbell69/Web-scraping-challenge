#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
from splinter import Browser

import pandas as pd


# In[2]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


#url = input('SENT FROM USER REQUEST')
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

browser.visit(url)
html = browser.html

soup = BeautifulSoup(html, 'html.parser')


# In[ ]:


# print(soup.prettify())


# In[4]:


# Find most recent article header
prep_news = soup.find("section", class_='grid_gallery').find("div", class_='list_text')

recent_news_title = prep_news.find("div", class_="content_title").text
recent_news_p = prep_news.find("div", class_="article_teaser_body").text
print(f"Most recent article title is: {recent_news_title}")
print(f"Most recent article title is: {recent_news_p}")


# # Feature image for Mars - Splinter

# In[5]:


url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url2)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[6]:


loc_image = soup.div.article['style']
# loc_image


# In[7]:


head, sep, tail = loc_image.partition("'")

# print (tail)


# In[8]:


url = tail

head, sep, tail = url.partition("'")

# print (head)


# In[9]:


featured_image_url = "https://www.jpl.nasa.gov" + head
print(featured_image_url)


# # Mars Weather from Twitter

# In[10]:


url3 = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url3)

html = browser.html
soup = BeautifulSoup(html, 'html.parser')


# In[11]:


recent_weather_tweet = soup.find("div", class_='js-tweet-text-container').text
recent_weather_tweet


# In[12]:


# Find most recent weather
if "InSight" in recent_weather_tweet : 

    if "hPapic" in recent_weather_tweet : 

        weather1 = (recent_weather_tweet.replace("hPapic", "hPa "))

        spl_word = 'hPa'

        weather_clean = weather1.partition(spl_word)[0]
        mars_weather = (weather_clean + "hPa")
        print(mars_weather)

else :
    print("No weather data yet")


# # Mars Facts

# In[ ]:


url4 = 'https://space-facts.com/mars/'


# In[ ]:


tables = pd.read_html(url4)
# tables


# In[ ]:


Mars_df = tables[0]
# Mars_df


# In[ ]:


Mars_df.columns = ['Description', 'Values']
Mars_df.to_html('Mars_Stats_table.html', index=False)


# # Mars hemispheres

# In[13]:


url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url5)


# In[14]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

Mars_hemi_data_list = []

for i in range(4):

    Mars_hemi_data = {}

    browser.find_by_css('img[class=thumb]')[i].click()

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    time.sleep(1)
    
    hemi_page = soup.find('div', class_='content')
    hemi_link_list = hemi_page.find('section', class_='block metadata')
    
    Mars_hemi_data['title'] = hemi_link_list.h2.text
    
    hemi_img_page = soup.find('div', class_='downloads')

    Mars_hemi_data['img_url'] = hemi_img_page.li.a['href']
    
    Mars_hemi_data_list.append(Mars_hemi_data)
    print(Mars_hemi_data)
    
    browser.back()
print(Mars_hemi_data_list)

# In[ ]:




