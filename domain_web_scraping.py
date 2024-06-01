from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import time

# Initialized the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), keep_alive=True)

# Loading the webpage
driver.get("https://www.domain.com.au/sale/?excludeunderoffer=1&suburb=epping-nsw-2121")

# Waiting for the page to load completely
time.sleep(5)

# saving the page source in html_content variable and parsing it
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

# Finding the <ul> tag containing all the property information
all_properties_ul_tag = soup.find('ul', class_='css-8tedj6')

# Ensuring the tag was found
if all_properties_ul_tag:
    # Find all <li> tags within the <ul> tag for individual property
    property_list_items = all_properties_ul_tag.find_all('li', class_='css-1qp9106')

    # Iterating over each <li> tag to scrape property information
    l = []
    for li_tag in property_list_items:
        o = {}
        try:
            o["Property address"] = li_tag.find('h2', {'class': 'css-bqbbuf'}).text.strip()
        except:
            o["Property address"] = None
        
        features_container = li_tag.find('div', {'data-testid': 'property-features-wrapper'})

        if features_container:
            feature_spans = features_container.find_all('span', {'data-testid': 'property-features-feature'})
            
            for feature_span in feature_spans:
                bedroom_span = feature_span.find('span', {'data-testid': 'property-features-text'})
                if bedroom_span and bedroom_span.text.strip() == "Beds":
                    # Extracting the number of bedrooms
                    beds_span = feature_span.find('span', {'data-testid': 'property-features-text-container'})
                    if beds_span:
                        o["Number of Bedrooms"] = beds_span.text.strip()
                    else:
                        o["Number of Bedrooms"] = None
                    break
        
        if features_container:
            feature_spans = features_container.find_all('span', {'data-testid': 'property-features-feature'})
            
            for feature_span in feature_spans:
                bathroom_span = feature_span.find('span', {'data-testid': 'property-features-text'})
                # Extracting the number of bathrooms
                if bathroom_span and bathroom_span.text.strip() == "Baths":
                    baths_span = feature_span.find('span', {'data-testid': 'property-features-text-container'})
                    if baths_span:
                        o["Number of Bathrooms"] = baths_span.text.strip()
                    else:
                        o["Number of Bathrooms"] = None
                    break
        
        if features_container:
            feature_spans = features_container.find_all('span', {'data-testid': 'property-features-feature'})
            
            for feature_span in feature_spans:
                parking_span = feature_span.find('span', {'data-testid': 'property-features-text'})
                # Extracting the number of parkings are there
                if parking_span and parking_span.text.strip() == "Parking":
                    parking_spaces_span = feature_span.find('span', {'data-testid': 'property-features-text-container'})
                    if parking_spaces_span:
                        o["Number of Parking Spaces"] = parking_spaces_span.text.strip()
                    else:
                        o["Number of Parking Spaces"] = None
                    break

        if features_container:
            feature_spans = features_container.find_all('span', {'data-testid': 'property-features-feature'})
            
            for feature_span in feature_spans:
                size_span = feature_span.find('span', {'data-testid': 'property-features-text-container'})
                # Extracting the Property Size area
                if size_span and "m²" in size_span.text:
                    o["Property Size"] = size_span.text.strip()
                    break
            
        else:
            o["Number of Bedrooms"] = None
            o["Number of Bathrooms"] = None
            o["Number of Parking Space"] = None
            o["Property Size"] = None

        try:
            o["Property Type"] = li_tag.find('div', {'class': 'css-11n8uyu'}).text.strip()
        except:
            o["Property Type"] = None

        try:
            o["Property Agent Name"] = li_tag.find('div', {'class': 'css-1t7a3eq'}).text.strip()
        except:
            o["Property Agent Name"] = None
        try:
            o["Property Price"] = li_tag.find('div', {'class': 'css-9hd67m'}).text.strip()
        except:
            o["Property Price"] = None

        l.append(o)

    # Printing the list of property details
    for i, property_detail in enumerate(l, start=1):
        print(i, property_detail)

    wb = Workbook()
    ws = wb.active

    headers = ["Property address", "Number of Bedrooms", "Number of Bathrooms", "Number of Parking Spaces", "Property Size", "Property Type", "Property Agent Name", "Property Price"]
    ws.append(headers)

    for property in l:
        # Retrieve property details
        address = property.get("Property address", "")
        bedrooms = property.get("Number of Bedrooms", "")
        bathrooms = property.get("Number of Bathrooms", "")
        parking_spaces = property.get("Number of Parking Spaces", "")
        size = property.get("Property Size", "")
        property_type = property.get("Property Type", "")
        agent_name = property.get("Property Agent Name", "")
        price = property.get("Property Price", "")
        
        ws.append([address, bedrooms, bathrooms, parking_spaces, size, property_type, agent_name, price])

    # Saving the workbook
    wb.save("property_details.xlsx")
    print("Data saved to property_details.xlsx")
else:
    print("Could not find the property list container.")

# Close the browser
driver.quit()
