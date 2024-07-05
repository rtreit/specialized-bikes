import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import json
import tabulate

async def fetch_page(session, page):
    url = f'https://www.specialized.com/us/en/c/bikes?page={page}'
    async with session.get(url) as response:
        return await response.text()

async def fetch_all_pages():
    tasks = []
    async with aiohttp.ClientSession() as session:
        for i in range(1, 100):
            tasks.append(fetch_page(session, i))
        return await asyncio.gather(*tasks)

def extract_data_from_page(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
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
        row['name'] = result['productData']['name']
        row['size'] = result['productData']['variant']
        row['class'] = result['productData']['dimension1']
        row['type'] = result['productData']['dimension2']
        row['subtype'] = result['productData']['dimension5']
        row['price'] = float(result['productData']['price'])
        data[id] = row
        id += 1
    return pd.DataFrame(data).T

async def main():
    pages = await fetch_all_pages()
    dfs = []
    for page in pages:
        json_data = extract_data_from_page(page)
        if json_data:
            df = parse_product_data(json_data)
            dfs.append(df)
    if dfs:
        df = pd.concat(dfs)
        df = df.sort_values(by='price', ascending=False).reset_index(drop=True)
        return df

# Run the main function using asyncio
df = asyncio.run(main())
# print df with tabulate
print(tabulate.tabulate(df, headers='keys', tablefmt='psql'))