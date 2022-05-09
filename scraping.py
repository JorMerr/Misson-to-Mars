# import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

# define scrape_all function
def scrape_all():

    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # set news title and paragraph variables
    news_title, news_paragraph = mars_news(browser)


    # run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    # stop webdriver and return data
    browser.quit()
    return data

# Define mars_news function
def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # set html parser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    # Add try/except for error handling
    try:
        # begin scraping
        slide_elem.find('div', class_='content_title')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    # if error, return None
    except AttributeError:
        return None, None


    # return news_title and news_p
    return news_title, news_p

# ## JPL Space Images Features Images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url
    

# Mars Facts
# define mars_facts function
def mars_facts():
    # Use try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # arrange the dataframe        
    df.columns = ['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # convert dataframe to HTML format, add bootstrap
    return df.to_html()

# Hemisphere Data
# define hemisphere function
def hemisphere(browser):
    # Visis URL
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # Create a list to hold images and titles
    hemisphere_image_urls = []

    # Parse the html with soup
    html_hemisphere = browser.html
    soup_hemisphere = soup(html_hemisphere, 'html.parser')

    # Retrieve the image urls and titles
    results = soup_hemisphere.find_all('div', class_='item')

    results_count = len(results)

    for result in range(results_count):
        # create dictionary to hold hemisphere data
        hemispheres = {}
        
        # find link for each hemisphere by text 'Hemisphere' and click
        browser.links.find_by_partial_text('Hemisphere')[result].click() 

        # try/except for error handling 
        try:
            # find title of article by tag and class  
            title = browser.find_by_css('h2.title').text

            # save to variable img_url for each full size image by searcing 'Sample' on new page
            img_url = browser.links.find_by_partial_text('Sample')['href']

            # append img_url and img_title to hemsipheres dictionary
            hemispheres["img_url"] = img_url
            hemispheres["title"] = title
            hemisphere_image_urls.append(hemispheres)

        except AttributeError:
            return None
        # return to main page
        browser.back()
    
    # return the list of hemisphere data
    return hemisphere_image_urls


if __name__ == "__main__":

    # if running as script, print scraped data
    print(scrape_all())