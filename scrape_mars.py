import pandas as pd
from splinter import Browser
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import pymongo
import time

def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    '''
    Scrape mars data from NASA website. Utilizing splinter, selenium, and BeautifulSoup.
    '''
    #Dictionary to store all output
    mars_dict = {}

    browser = init_browser()
    #Mars News url
    news_url = 'https://mars.nasa.gov/news'
    #Browser setup
    browser.visit(news_url)
    #Create BeautifulSoup object and parse
    soup = bs(browser.html, 'html.parser')
    #Latest news title
    news_title = soup.find(class_='content_title').get_text(strip=True)
    #Paragraph from title
    news_p = soup.find(class_='article_teaser_body').get_text(strip=True)
    #Add data to mars_dict
    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    #JPL Mars Space Images - Featured Image
    #Create new url_path
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url ="https://www.jpl.nasa.gov"
    #Browser setup
    browser.visit(jpl_url)
    #Utilize Browser objects to manipulate website
    browser.is_element_present_by_id("full_image")
    browser.click_link_by_id("full_image")
    #Utilize Browser objects to manipulate website
    browser.is_element_present_by_text("more info")
    browser.click_link_by_partial_text('more info')
    #Create BeautifulSoup and parse;
    html = browser.html
    featured_image_soup = bs(html,"html.parser")
    #Obtain image href, alt description, and connect to url
    featured_image = featured_image_soup.find(class_="lede")
    featured_image_alt = featured_image.a.img['alt']
    featured_image_url = (base_url + featured_image.a["href"])
    #Add data to mars_dict
    mars_dict['featured_image_url'] = featured_image_url
    mars_dict['featured_image_alt'] = featured_image_alt

    #Mars Weather
    #Create new url_path
    tweeter_url = "https://twitter.com/marswxreport?lang=en"
    #Browser setup
    browser.visit(tweeter_url)
    #Create BeautifulSoup and parse;
    html = browser.html
    tweet_soup = bs(html, 'html.parser')
    #Obtain and asign mars_weather result
    mars_weather = tweet_soup.find(class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text(strip=True)
    #Add data to mars_dict
    mars_dict['mars_weather'] = mars_weather

    #Mars Facts
    #Create new url_path
    planet_facts_url = "https://space-facts.com/mars/"
    #Browser setup
    browser.visit(planet_facts_url)
    data = pd.read_html(planet_facts_url)
    data = data[0]
    data.columns = ['Description', 'Info']
    data = data.to_html(index=False)
    data = data .replace('\n', '')
    #Add data to mars_dict
    mars_dict['data'] = data

    #Mars Hemispheres
    #Create new url_path
    mars_hem = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    base_url = "https://astrogeology.usgs.gov/"
    #Browser setup
    browser.visit(mars_hem)
    html = browser.html
    mars_hem_soup = bs(html, 'html.parser')
    mars_data = mars_hem_soup.find_all(class_='itemLink product-item')
    #Generate empty lists
    hemisphere_image_urls = []
    hemisphere_dict = {}

    for link in range(0,len(mars_data),2):
        #Visit each hemisphere url
        browser.visit(base_url + mars_data[link]["href"])
        #Convert page to html to parse title
        html = browser.html
        mars_hem_soup = bs(html, "html.parser")
        #Scrape for text
        #Extract title from h2 tag
        hemisphere_title = mars_hem_soup.find("h2", class_="title").text
        #Look for 'sample' button that contains our image links
        sample_button = browser.find_link_by_text("Sample").first
        #Save image links to our list
        hemisphere_dict = {"title": hemisphere_title, "img_url": sample_button["href"]}
        hemisphere_image_urls.append(hemisphere_dict)

    #Close open browser
    browser.quit()

    #Add data to mars_dict
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict

if __name__ == "__main__":
    data = scrape()
    print(data)