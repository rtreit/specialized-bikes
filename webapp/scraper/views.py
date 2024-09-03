import pandas as pd

from django.core.exceptions import ObjectDoesNotExist # TODO: replace with custom exception
from django.shortcuts import render
from .services.get_bikes import fetch_all_pages, extract_data_from_page, parse_product_data

# Create your views here.
async def scrape_specialized(request):
    try:
        pages = await fetch_all_pages()
        dfs = []
        for page in pages:
            json_data = extract_data_from_page(page)
            if json_data is not None:
                df = parse_product_data(json_data)
                if df is not None:
                    dfs.append(df)
        if len(dfs) > 0:
            df = pd.concat(dfs)
            df = df.sort_values(by='price', ascending=False).reset_index(drop=True)
            # bikes_data is a list of python dictionaries
            # dictionary keys are: 'name', 'size', 'class', 'type', 'subtype', 'price'
            bikes_data = df.to_dict(orient='records') 
        else:
            raise Exception("No data found in the pages")

    except Exception as e:
        print(f"Error: {str(e)}") # TODO: add logging in settings.py
        raise ObjectDoesNotExist("Error fetching data from Specialized website")

    return render(request, 'scraper/scrape_specialized.html', context={'bikes': bikes_data})

def home(request):
    return render(request, 'scraper/home.html')
