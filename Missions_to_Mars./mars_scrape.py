import splinter 
import selenium 
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import time

def init_browser():
    #starting the browser
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
def scrape():
    
    browser = init_browser()
##GET THE TITTLE AND SUMMARY    
#go to the url nasa mars page to web scrape
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    time.sleep(2)


#get html code from the webpage and parse it 
    html = browser.html
    soup = BeautifulSoup(html,'html.parser')

#get the first news title and first news summary 
    result = soup.find('div',  class_ = 'list_text')

    news_title = result.find('a', target = '_self').text
    news_p = result.find('div', class_='article_teaser_body').text

#GET Featured Image
#go to the url for the featured image 
    url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url2)
#get html code from it 
    html2 = browser.html
    soup2 = BeautifulSoup(html2,'html.parser')

#get the ending of the url to link to the image 
    result2 = soup2.find('article',  class_ = 'carousel_item')
# Identify and return link to listing
    link = result2.a['data-fancybox-href']

    featured_image_url = 'https://www.jpl.nasa.gov+link'+ link

#Get Last tweet
# go to the twitter of mars weather 
    # go to the twitter of mars weather 
    url3 = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url3)
    time.sleep(2)

#get html code from it 
    html3 = browser.html
    soup3 = BeautifulSoup(html3,'html.parser')

#get the first tweet on the page 
    mars_weather = soup3.find('span',  class_ = 'css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0').text
    #mars_weather = result3.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

# go to the url to get mars facts
    
    url4 = 'https://space-facts.com/mars/'
    #get html code from it 
    df = pd.read_html(url4)[0]
    df.columns=["Description", "Value"]
    df.set_index("Description", inplace=True)
    mars_data = df.to_html(classes="table table-striped")
# go to the url to get Mars Hemispheres images
    url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url5)

#get html code from it 
    html5 = browser.html
    soup5 = BeautifulSoup(html5,'html.parser')

#find all  the listings in the html 
    result5 = soup5.find_all('div', class_="item")

#Create an empty list 
    hemisphere_image_urls = []
# iterate through the four results and go to their link to get the image url
    for result in result5:
        link = result.a['href']
        browser.visit('https://astrogeology.usgs.gov'+link)
        html6 = browser.html
        soup6 = BeautifulSoup(html6,'html.parser')
        first = soup6.find('div',class_="downloads")
        image_url = first.a['href']
        title = soup6.find('h2', class_= 'title').text
        post = {"title": title, "img_url": image_url }
        hemisphere_image_urls.append(post)
        browser.back()

    mars_info_dict = {"news_title":news_title,"news_text":news_p,
    "featured_image":featured_image_url,"mars_weather":mars_weather,
    "mars_facts":mars_data,"hemisphere_image_urls":hemisphere_image_urls}

    return mars_info_dict

