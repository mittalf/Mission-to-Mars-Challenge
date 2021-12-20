# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    news_title, news_paragraph = mars_news(browser)
    #hemispheres = ars_hemispheres(browser)m
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres" : mars_hemispheres(browser)
        #{ "img_url" : hemisphere.img_url, "title": hemisphere.title }
        }
            
    

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")




# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres
def mars_hemispheres(browser):

    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    images_list = []
    titles = []
    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    html = browser.html
    hem_soup = soup(html, 'html.parser')
    
    desc_items = hem_soup.find_all('div',class_='description')
    
    for hem_item in desc_items:
        #print(hem_item)
    
        link = hem_item.a['href']
        new_link = browser.url + link
        next_html_page = f'{new_link}' 
           
        # add url to the list
        images_list.append(next_html_page)
    
    
    # Import Splinter and BeautifulSoup
    from splinter import Browser
    from bs4 import BeautifulSoup as soup1
    from webdriver_manager.chrome import ChromeDriverManager
    import requests

    for images in images_list:
       
        hemispheres = {}
    
        #browser.visit(images)
        
        #html = browser.html
        html = images
      
        response = requests.get(html)
        img_soup = soup1(response.text, 'html.parser')
           
        desc_items = img_soup.find('div',class_='container')
      
        # location to image    
        desc_items2 = desc_items.find('div',class_='wide-image-wrapper')
        desc_items3 = desc_items2.find('div',class_='downloads')
        desc_items4 = desc_items3.find('ul')
        desc_items5 = desc_items4.find('li')
        desc_items6 = desc_items5.find('a')
        href = desc_items5.a['href']
        image_url = "https://marshemispheres.com/" + href
              
        # get title
    
        title_items1 = desc_items.find('div',class_='cover')
        titles = img_soup.find('h2').text        
        
        hemispheres["img_url"] = image_url
        hemispheres["title"] = titles
            
        hemisphere_image_urls.append(hemispheres)

        hemisphere_image_urls
        
    
        browser.back()
      
        
    return hemisphere_image_urls


    if __name__ == "__main__":

    # If running as script, print scraped data
        print(scrape_all())