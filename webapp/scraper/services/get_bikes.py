import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import json

# TODO: Add logging in stettings.py and replace print statements with logging

async def fetch_page(session, page):
    url = f'https://www.specialized.com/us/en/c/bikes?page={page}'
    async with session.get(url) as response:
        response = await response.text()
        if not response:
            raise Exception('No response from', url)
        return response

async def fetch_all_pages():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 15): # TODO: Use breadcrumbs to determine the number of pages
            tasks.append(fetch_page(session, i))
            await asyncio.sleep(0.1) # sleep for .1 seconds between calls
        return await asyncio.gather(*tasks)

def extract_data_from_page(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    title_tag = soup.find('title')
    if title_tag is not None and "access denied" in title_tag.text.lower():
        print('access denied')
    for script in soup.find_all('script'):
        if script.get('id') == '__NEXT_DATA__':
            script_text = script.text
            json_data = json.loads(script_text)
            return json_data
    return None

def parse_product_data(json_data):
    data = {}
    id = 1
    for result in json_data['props']['pageProps']['initialProductData']['results']:
        row = {}
        if result.get('productData') is not None:
            row['name'] = result['productData']['name']
            row['size'] = result['productData']['variant']
            row['class'] = result['productData']['dimension1']
            row['type'] = result['productData']['dimension2']
            row['subtype'] = result['productData']['dimension5']
            row['price'] = float(result['productData']['price'])
            data[id] = row
            id += 1
        else:
            print('No product data found')
    if not data:
        return None
    return pd.DataFrame(data).T