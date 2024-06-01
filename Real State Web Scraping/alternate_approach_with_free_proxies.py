import requests
import random
from bs4 import BeautifulSoup as bs
import traceback

def get_free_proxies():
    url = "https://free-proxy-list.net/"
    soup = bs(requests.get(url).content, 'html.parser')
    proxies = []
    for row in soup.find("table", attrs={"class": "table-striped"}).find_all("tr")[1:]:
        tds = row.find_all("td")
        try:
            ip = tds[0].text.strip()
            port = tds[1].text.strip()
            proxies.append(str(ip) + ":" + str(port))
        except IndexError:
            continue
    return proxies

def scrape_real_estate(proxies):
    url = "https://www.realestate.com.au/buy/in-epping/list-1"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    for i in range(len(proxies)):
        print("Request Number : " + str(i+1))
        proxy = proxies[i]
        try:
            response = requests.get(url, headers=headers, proxies={"http": proxy, "https": proxy}, timeout=5)
            if response.status_code == 200:
                soup = bs(response.content, 'html.parser')
                print(soup.prettify()[:1000])
                return soup
            else:
                print(f"Failed with status code {response.status_code}")
        except Exception as e:
            print(f"Failed with proxy {proxy}. Error: {e}")
            continue

proxies = get_free_proxies()
soup = scrape_real_estate(proxies)

if soup:
    try:
        all_properties_ul_tag = soup.find('ul', class_='tiered-results tiered-results--exact')
        property_list_items = all_properties_ul_tag.find_all('article', class_='residential-card')

        properties = []
        for item in property_list_items:
            property_data = {}
            property_data["address"] = item.find('h2', class_='residential-card__address-heading').text.strip()
            property_data["price"] = item.find('span', class_='property-price').text.strip()
            properties.append(property_data)

        for property in properties:
            print(property)
    except Exception as e:
        print(f"Error extracting property data: {e}")