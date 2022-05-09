# Misson-to-Mars

## Purpose of the Project
The purpose of this project is to build a porfolio website which will scrape various web sources at the click of a button and generate information and images related to Mars. 

## Methods Used and Scraping Sources
The project is built primarly with Python, but testing and development was done in Jupyter Notebooks. The Python script uses:
- Splinter
- BeautifulSoup
- Webdriver
- Pandas
- Datetime
- Flask
- PyMongo
- Bootstrap3

The functions in `scraping.py` automate the navigation to, and collection of, information related to Mars.

The first website visted is https://redplanetscience.com to gather the most recent available article title, and summary paragraph content. 

The next website visted is https://spaceimages-mars.com to scrape the most recent Featured Image at the full size and return the full image URL.

The third website visted is https://galaxyfacts-mars.com where the script reads the Mars vs Earth comparison table and saves it as a Pandas DataFrame.

The final website visted is https://marshemispheres.com where our script clicks the link to each article on the page, then searches that page for the full image URL, and the Article Title, saving it to a key:value pair before returning to the main page and moving to the next article. Each key:value pair is saved to a list of dictionaries.

The functions in `app.py` create the Flask website, and configure the MongoDB database where our scraped data is stored. The root route of the application references the `index.html` template within the templates directory of our repository.

Built into the Flask website is a button which initiates the scraping process and navigates to the /scrape page of the Flask website. Once the scraping is completed, the Flask website is automatically redirected back to the root route of the application with all the collected data displayed.

Within the `index.html` template, the project uses the Bootstrap3 styling settings, with some additional configuration options: 
- The button to "Scrape New Data" will display as a different colour when hovered over. 
- The Mars Hemisphere images have been styled as thumbnail images.