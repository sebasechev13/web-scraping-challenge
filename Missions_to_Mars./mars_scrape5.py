import pandas as pd 
import selenium
import splinter
from bs4 import BeautifulSoup
from splinter import Browser
import requests

def init_browser():
    #starting the browser
    executable_path = {'executable_path':'/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=True)

##start the webscraping functinon
def scrape():
    browser= init_browser()
    ##calling the function to start the browser made above
    #get the title and summary of first news article on nasa website
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    html = requests.get(url)
    #get the htmle code form webpage and parse it
    soup = BeautifulSoup(html,'html.parser')
    #get the first new title and first news summary
    result = soup.find('div', class_ ='list_text')
    news_title = result.find('div', target = 'content_title').text
    news_link = result.a['href']
    news_p = result.find('div', class_ ='article_teaser_body').text 
    news_date = result.find('div', class_ ='list_date').text 
    #get the featured Image url
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)

    #get html code from it 
    html2 = browser.html
    soup2 = BeautifulSoup(html2,'html.parser')

    #get the ending of the url to link the image
    result2 = soup2.find('article', class_ = "carousel_item")
    #identify and reutnr link to listing 
    link = result2.a['data-fancybox-href']
    featured_image_url = 'https://www.jpl.nasa.gov/'+link

    #ge the text from the first tweet on mars weather 
    html = requests.get('https://twitter.com/marswxreport?lang=en').text
    html1 = BeautifulSoup(html,'html.parser')
    news1 = html1.find('p',  class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    next_text = news1.text
    news5 = news1.find_all("a")
    text=("")
    text1=("")
    for news in news5:
        text1 = news.text
        text = text+text1
    mars_weather = next_text.replace(text,'')   

    

    #read html to get mars facts
    mars_df = pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns = ['Description', 'Value']
    mars_df = mars_df.set_index("Description", inplace = True)
    mars_data = mars_df.to_html(classes="table table-striped")

    #go to the url to get Mars Hemisphere images 
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

    #get html code from it 
    html5 = browser.html
    soup5 = BeautifulSoup(html5, 'html.parser')
    #find all the listings in the html
    result5 = soup5.find_all('div', class_='item')

    #create an empty list 
    hemisphere_image_urls =[]
    #iterate through the four results and go to their link to get the image url
    for result in result5:
        link = result.a['href']
        browser.visit('https://astrogeology.usgs.gov'+link)
        html6 = browser.html
        soup6 = BeautifulSoup(html6,'html_parser')
        first = soup6.find('div', class_ = 'downloads')
        image_url =first.a['href']
        title = soup6.find('h2', class_ ='title').text
        post = {'title': title, 'img_url': image_url}
        hemisphere_image_urls.append(post)
        browser.back
    mars_info_dict = {"news_title":news_title,"news_text":news_p,"news_date":news_date,"news_link":news_link,
    "featured_image":featured_image_url,"mars_weather":mars_weather,
    "mars_facts":mars_data,"hemisphere_image_urls":hemisphere_image_urls}

    return mars_info_dict



