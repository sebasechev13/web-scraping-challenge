import pandas as pd 
import selenium
import splinter
from bs4 import BeautifulSoup as bs 
from splinter import Browser
import requests
import time
import tweepy
import json
import re
from tweepy import OAuthHandler

import twitter_credentials

def init_browser():
    #starting the browser
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

def close_browser(browser):
    browser.quit()

def scrape_all():
    mars = {}
    mars['news_info'] = scrape_news()
    mars['feat_img'] = f_img()
    mars['twitter'] = twitter()
    mars['data_table'] = table()
    mars['hemisphere_image_urls'] = mars_h_images()
    return  mars
def scrape_news():
    try:
        ## initialize browser and latest_news dict
        browser = init_browser()
        latest_news={}


        ## define url and command browser to visit and parse HTML for posts tag   
        nasa_url= "https://mars.nasa.gov"
        news_url= "https://mars.nasa.gov/news/"
        browser.visit(news_url)
        time.sleep(1)
    
        html = browser.html
        soup = bs(html, "html.parser")
        try:
            #find first news article 
            news = soup.find('div', class_='list_text')

        
            ## collect title, date, description and link of post
            titles = news.find('div', class_='content_title').text
            date = news.find('div', class_='list_date').text
            news_p = news.find('div', class_='article_teaser_body').text
            link = news.a['href']
            ## run it untill the attribute error doesnt show up. 
        except AttributeError:
            print("error")
            
            

        ## add results to latest_news dictionary
        latest_news['news_title'] = titles
        latest_news['news_date'] = date
        latest_news['news_about'] = news_p
        latest_news["news_link"] = f'{nasa_url}{link}'
        return latest_news
    
## close browser    
    finally:        
        close_browser(browser)
def f_img():
    try:
        browser = init_browser()

        url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        browser.visit(url2)

        #get html code from it 
        html2 = browser.html
        soup2 = bs(html2,'html.parser')

        #get the ending of the url to link the image
        result2 = soup2.find('article', class_ = "carousel_item")
        #identify and reutnr link to listing 
        link = result2.a['data-fancybox-href']
        featured_image_url = f'https://www.jpl.nasa.gov{link}'
        return featured_image_url

    finally:        
        close_browser(browser)

def twitter():
    # set up dict
    mars_weather = {}
    # set up the authication fro the twitter API
    auth = tweepy.OAuthHandler(twitter_credentials.Cons_API_key, twitter_credentials.Cons_API_secret_key )
    auth.set_access_token(twitter_credentials.Access_token, twitter_credentials.Access_token_secret)
    #chose the API of twitter which we will use JSO 
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    target_user = "MarsWxReport"
    tweet = api.user_timeline(target_user, count =0, page = 0)
    link = ((tweet)[0]['entities']['urls'][0]['url'])
    mars_weather['link'] = link
    text = ((tweet)[0]['text'])
    mars_weather['tweet'] = text.replace(link,"")



    return mars_weather
def table():
     #read html to get mars facts
    mars_facts =("")
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df = pd.DataFrame(mars_df)
    mars_df.columns = ['Description', 'Value']
    mars_df = mars_df.set_index("Description", inplace = True)
    mars_facts = mars_df.to_html(index = True, header = True, classes="table table-striped")
    return mars_facts
def mars_h_images():
    try:
        browser = init_browser()
        #go to the url to get Mars Hemisphere images 
        url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url5)

        #get html code from it 
        html2 = browser.html
        soup5 = bs(html2, "html.parser")
        #find all the listings in the html
        result5 = soup5.find_all('div', class_='item')
         #create an empty list 
        hemisphere_image_urls =[]
        #iterate through the four results and go to their link to get the image url
        for result in result5:
            link = result.a['href']
            browser.visit('https://astrogeology.usgs.gov'+link)
            html6 = browser.html
            soup6 = bs(html6,'html.parser')
            first = soup6.find('div', class_ = 'downloads')
            image_url =first.a['href']
            title = soup6.find('h2', class_ ='title').text
            post = {'title': title, 'img_url': image_url}
            hemisphere_image_urls.append(post)
            browser.back
        return hemisphere_image_urls
    finally:        
        close_browser(browser)