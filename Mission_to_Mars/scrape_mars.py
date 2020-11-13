from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'C:\\Users\\capfl\\.wdm\\drivers\\chromedriver\\win32\\86.0.4240.22\\chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)
    
mars_data = []

def news_scrape():
        browser = init_browser()

        url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        news_title = soup.find_all('div', class_='content_title')[1].text

        paragraph_txt = soup.find_all('div', class_='article_teaser_body')[0].text
        
        mars_data.append({
            "news_title": news_title,
            "news_text": paragraph_txt
            })

        return mars_data

def featured_image_scrape():
        browser= init_browser()

        jpl_mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

        browser.visit(jpl_mars_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        feature = soup.find_all('a', class_= "button fancybox")[0]
        feature_img = feature['data-fancybox-href']
        featured_image_url = jpl_mars_url + feature_img


        mars_data.append({
            "featured_image": featured_image_url
            })
        return mars_data

def facts_scrape():

        facts_url = 'https://space-facts.com/mars/'

        facts_df = pd.read_html(facts_url)[0]
        facts_df.columns = ['Description','Value']

        html_table = facts_df.to_html().replace('\n', '')
        facts_df.replace('\n', '').to_html('table.html')
       
        mars_data.append({
            "mars_facts": html_table
            })
        return mars_data

def hemisphere_url_scrape():
        browser= init_browser()

        basic_hemisphere_url = 'https://astrogeology.usgs.gov'
        hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        
        browser.visit(hemisphere_url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')   

        all_hemispheres = soup.find_all('div', class_= 'description')

        hemisphere_image_urls= []

        for hemisphere in all_hemispheres:
    
            title = hemisphere.h3.text
    
            hemisphere_url = hemisphere.a.get('href')
            hemisphere_link = (basic_hemisphere_url + hemisphere_url)

         # Needs this path written out every time for some reason
            executable_path = {'executable_path': 'C:\\Users\\capfl\\.wdm\\drivers\\chromedriver\\win32\\86.0.4240.22\\chromedriver.exe'}
            browser = Browser('chrome', **executable_path, headless=False)
    
            browser.visit(hemisphere_link)
            link_html = browser.html
            link_soup = BeautifulSoup(link_html, 'html.parser')
    
            image_url = link_soup.find("img", class_= "thumb")['src']
    
            hemisphere_image_urls.append({"title" : title, "img_url" : image_url})


            mars_data.append({
                "hemisphere_images": hemisphere_image_urls
                })
        return mars_data
        