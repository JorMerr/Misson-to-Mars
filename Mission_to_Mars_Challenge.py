#!/usr/bin/env python
# coding: utf-8

# In[105]:


# import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[106]:


# set executable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[107]:


# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)

# optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[108]:


# set html parser
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')


# In[109]:


# begin scraping
slide_elem.find('div', class_='content_title')


# In[110]:


# Use the parent element to find the first 'a' tag and save it as 'news_title'
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[111]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured Images

# In[112]:


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# In[113]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[114]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[115]:


# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[116]:


# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ## Mars Facts

# In[117]:


# begin scrape of table 
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns = ['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[118]:


df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# In[119]:


# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)


# In[120]:


html = browser.html
soup = soup(html, 'html.parser')


# In[121]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

results = soup.find_all('div', class_='item')

results_count = len(results)

for result in range(results_count):
    # create dictionary to hold hemisphere data
    hemispheres = {}
    
    # find link for each hemisphere by text 'Hemisphere' and click
    browser.links.find_by_partial_text('Hemisphere')[result].click()  

    # find title of article by tag and class  
    title = browser.find_by_css('h2.title').text
    # print(title)
    
    # save to variable img_url for each full size image by searcing 'Sample' on new page
    img_url = browser.links.find_by_partial_text('Sample')['href']
    # print(img_url)
    
    
    # append img_url and img_title to hemsipheres dictionary
    hemispheres["img_url"] = img_url
    hemispheres["title"] = title
    hemisphere_image_urls.append(hemispheres)
    # print(hemisphere_image_urls)
    
    # return to main page
    browser.back()


# In[122]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[123]:


# 5. Quit the browser
browser.quit()

