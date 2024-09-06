import logging
import json
from bs4 import BeautifulSoup

from django.utils import timezone


from scraper.models import SpecializedBike
from core.rest_client import RestClient


logger = logging.getLogger("scraper")

def fetch_all_pages():
    pages = []
    # TODO: Use while loop to stop once no more bikes are found
    for i in range(1, 15): 
        pages.append(fetch_page(i))
    return pages

def fetch_page(page):
    client = RestClient()
    url = f"https://www.specialized.com/us/en/c/bikes?page={page}"
    response = client.make_request(url, "get")
    if not response:
        raise Exception(f"No response from {url}")
    return response.text

def extract_data_from_page(html_doc):
    soup = BeautifulSoup(html_doc, "html.parser")
    title_tag = soup.find("title")
    if title_tag is not None and "access denied" in title_tag.text.lower():
        logger.error("access denied")
    for script in soup.find_all("script"):
        if script.get("id") == "__NEXT_DATA__":
            script_text = script.text
            json_data = json.loads(script_text)
            return json_data
    return None

def parse_product_data(json_data):
    data = []
    for result in json_data["props"]["pageProps"]["initialProductData"]["results"]:
        row = {}
        if result.get("productData") is not None:
            row["url"] = "https://www.specialized.com" + result.get("url")
            row["name"] = result["productData"]["name"]
            row["size"] = result["productData"]["variant"]
            row["bike_class"] = result["productData"]["dimension1"]
            row["type"] = result["productData"]["dimension2"]
            row["subtype"] = result["productData"]["dimension5"]
            row["price"] = float(result["productData"]["price"])
            data.append(row)
        else:
            logger.info("No product data found")
    if not data:
        return None
    return data

def save_bikes_to_database(bikes):
    for bike in bikes:
        SpecializedBike.objects.create(**bike)
        
def do_scrape():
    logger.info(f"rescraping bikes ... ")
    pages = fetch_all_pages()
    all_bikes = []
    for page in pages:
        json_data = extract_data_from_page(page)
        if json_data is not None:
            bikes_on_page = parse_product_data(json_data)
            if bikes_on_page is not None:
                all_bikes.extend(bikes_on_page)
            for bike in all_bikes:
                logger.info(f"scraped new bike {str(bike)}\n \n")
    save_bikes_to_database(all_bikes)