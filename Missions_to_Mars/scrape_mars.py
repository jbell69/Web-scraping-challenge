import requests, re
from bs4 import BeautifulSoup
from splinter import Browser
import time
import pandas as pd


def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    # Featured article
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Find most recent article header and paragraph
    prep_news = soup.find("section", class_="grid_gallery").find(
        "div", class_="list_text"
    )

    recent_news_title = prep_news.find("div", class_="content_title").text
    recent_news_p = prep_news.find("div", class_="article_teaser_body").text

    # Feature image for Mars - Splinter
    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    loc_image = soup.div.article["style"]

    head, sep, tail = loc_image.partition("'")

    url = tail
    head, sep, tail = url.partition("'")

    featured_image_url = "https://www.jpl.nasa.gov" + head

    # Mars Weather from Twitter
    url3 = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url3)

    page = requests.get(url3).text
    soup = BeautifulSoup(page, "lxml")
    mars_weather = soup.findAll(string=re.compile("InSight", re.IGNORECASE))[0]
    print(mars_weather)
    # html = browser.html
    # soup = BeautifulSoup(html, "html.parser")

    # recent_weather_tweet = soup.find("div", class_="js-tweet-text-container").text

    # mars_weather = "No weather data yet"

    # if "InSight" in recent_weather_tweet:

    #     if "hPapic" in recent_weather_tweet:

    #         weather1 = recent_weather_tweet.replace("hPapic", "hPa ")

    #         spl_word = "hPa"

    #         weather_clean = weather1.partition(spl_word)[0]
    #         mars_weather = weather_clean + "hPa"
    #         print(mars_weather)

    # else:
    #     print(mars_weather)

    # Mars Facts
    url4 = "https://space-facts.com/mars/"

    tables = pd.read_html(url4)
    Mars_df = tables[0]
    Mars_df.columns = ["Description", "Values"]
    Mars_fact_table = Mars_df.to_html(index=False)

    # Mars hemispheres
    url5 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url5)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    Mars_hemi_data_list = []

    for i in range(4):

        Mars_hemi_data = {}

        browser.find_by_css("img[class=thumb]")[i].click()

        html = browser.html
        soup = BeautifulSoup(html, "html.parser")

        time.sleep(1)

        hemi_page = soup.find("div", class_="content")
        hemi_link_list = hemi_page.find("section", class_="block metadata")

        Mars_hemi_data["title"] = hemi_link_list.h2.text

        hemi_img_page = soup.find("div", class_="downloads")

        Mars_hemi_data["img_url"] = hemi_img_page.li.a["href"]

        Mars_hemi_data_list.append(Mars_hemi_data)
        print(Mars_hemi_data)

        browser.back()

    print(recent_news_title)
    print(recent_news_p)
    print(featured_image_url)
    print(mars_weather)
    print(Mars_hemi_data_list)

    Mars_scraped_data = {
        "recent_news_title": recent_news_title,
        "recent_news_p": recent_news_p,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "Mars_hemi_data_list": Mars_hemi_data_list,
        "Mars_fact_table": Mars_fact_table,
    }

    # Close the browser after scraping
    browser.quit()

    return Mars_scraped_data
