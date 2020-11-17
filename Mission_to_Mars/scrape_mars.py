#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import pandas as pd
import requests as req
from splinter import Browser
import pprint

def scrape():

    main_dict = {}
    
    # Defines "url" as variable to be used for provided website.

    url = "https://mars.nasa.gov/news/"

    # Brings up most recent NASA news in Google Chrome

    executable_path = {'executable_path':r"C:\Users\Patrick\GT-HW-Repo\Web_Scraping_HW\Web_Scraping_Challenge\Mission_to_Mars\chromedriver.exe"}
    browser = Browser("chrome",**executable_path)
    browser.visit(url)

    # Defines content as html object

    content = browser.html   

    # Newest Title
    headlines = browser.find_by_css("div[class='content_title']")
    #headlines[1].value

    # Assign variable to newest title
    new_headline = headlines[1].value
    #new_headline
    main_dict['new_headline'] = new_headline

    # Newest Title's paragraph text
    paragraphs = browser.find_by_css("div[class='article_teaser_body']")
    #paragraphs[0].value

    # Assign variable to newest title's paragraph text
    new_paragraph = paragraphs[0].value
    #new_paragraph
    main_dict['new_paragraph'] = new_paragraph

    # Use splinter to navigate to site
    # Visit the url for JPL Featured Space Image [here](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).

    url2 = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url2)

    # Assign content variable to browser.html
    content = browser.html

    #soup = BeautifulSoup(content, 'html.parser')

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    #    and assign the url string to a variable called `featured_image_url`.

    featured_image_object = browser.find_by_id('full_image')
    browser.click_link_by_id("full_image")

    # Navigate to url by clicking "More Info Button" 
    browser.click_link_by_partial_href('/spaceimages/details.php?id=')

    # Inspect the image required
    image_array = browser.find_by_css('img[class="main_image"]')
    

    # Copy full size image link provided in web objects elements
    # Make sure to save a complete url string for this image.
    featured_image_url = image_array[0]["src"]
    main_dict['featured_image_url'] = featured_image_url

    # Visit the Mars Facts webpage [here](https://space-facts.com/mars/)
    # and use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc.

    # Webpage url                                                                                                               
    space_facts_url = 'https://space-facts.com/mars/'

    # Extract tables
    df_list = pd.read_html(space_facts_url)

    # Get first table   
    # Note before submission clear index and headers
    df = df_list[0]
    

    # Use Pandas to convert the data to a HTML table string.
         #df.to_html()
    # Added (index = false, header = false to correctly render table)
    main_dict['table'] = df.to_html(index=False,header=False)
    

    # Visit the USGS Astrogeology site [here]
    # (https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) 
    # to obtain high resolution images for each of Mars's hemispheres.

    # Visit above link, scrape 4 url's by scraping webpage of four hyperlinks
    url3 = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url3)

    # Create a list of objects where class = "item"
    hemi_links = browser.find_by_css("div[class='item'] a")
    # hemi_links[0].href
    links_set = set()
    for i in hemi_links:
        #print(i["href"])
        links_set.add(i["href"])

    # Loop through each hyperlink in links_set and 
    hemisphere_image_urls = []

    for link in links_set:
        browser.visit(link)

        # Save both the image url string for the full resolution hemisphere image, 
        #     and the Hemisphere title containing the hemisphere name. 
        #     Use a Python dictionary to store the data using the keys `img_url` and `title`.
        
        # Get the page title
        title = browser.title 

        # Get the url for the image to inspect on page and grab it
        url_image = browser.find_link_by_text("Sample").first["href"]
        print(url_image)
        
        # Add the title and url to the list of dictionaries
        hemisphere_image_urls.append({"title": title, "img_url": url_image})

    main_dict['hemisphere_image_urls'] = hemisphere_image_urls
    #print(hemisphere_image_urls)

    return main_dict