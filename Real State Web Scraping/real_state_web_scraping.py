from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from openpyxl import Workbook
import time

# Initialize the WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), keep_alive=True)

# Load the webpage
driver.get("https://www.realestate.com.au/buy/in-epping/list-1")

# Wait for the page to load completely
time.sleep(5)

html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

all_properties_ul_tag = soup.find('ul', class_='tiered-results tiered-results--exact')

if all_properties_ul_tag:
    property_list_items = all_properties_ul_tag.find_all('article', class_='residential-card__property-card')

    l = []
    for li_tag in property_list_items:
        o = {}
        try:
            o["Property address"] = li_tag.find('h2', {'class': 'residential-card__address-heading'}).text.strip()
        except:
            o["Property address"] = None
        try:
            o["Number of Bedrooms"] = li_tag.find('span', {'aria-label':'Bedrooms'}).text.strip()
        except:
            o["Number of Bedrooms"] = None
        try:
            o["Number of Bathrooms"] = li_tag.find('span', {'aria-label':'Bathrooms'}).text.strip()
        except:
            o["Number of Bathrooms"] = None
        try:
            o["Number of Parking Space"] = li_tag.find('span', {'aria-label':'Car Spaces'}).text.strip()
        except:
            o["Number of Parking Space"] = None
        try:
            o["Property Type"] = li_tag.find('span', {'class':'residential-card__property-type'}).text.strip()
        except:
            o["Property Type"] = None
        try:
            o["Property Price"] = li_tag.find('span', {'class':'property-price'}).text.strip()
        except:
            o["Property Price"] = None
        try:
            o["Property Size"] = li_tag.find('span', {'class':'residential-card__land-area'}).text.strip()
        except:
            o["Property Size"] = None
        try:
            o["Property Agent Name"] = li_tag.find('span', {'class':'agent__name'}).text.strip()
        except:
            o["Property Agent Name"] = None

        l.append(o)

    # Print the list of property details
    for i, property_detail in enumerate(l, start=1):
        print(i, property_detail)

    # Save data to Excel file
    wb = Workbook()
    ws = wb.active

    # Write headers
    headers = ["Property address", "Number of Bedrooms", "Number of Bathrooms", "Number of Parking Space", "Property Type", "Property Price", "Property Agent Name"]
    ws.append(headers)

    # Write data
    for property in l:
        ws.append([property.get(header, "") for header in headers])

    # Save workbook
    wb.save("property_details.xlsx")
    print("Data saved to property_details.xlsx")
else:
    print("Could not find the property list container.")

# Close the browser
driver.quit()
