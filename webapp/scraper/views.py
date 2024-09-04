import pandas as pd

from asgiref.sync import sync_to_async

from django.db import DatabaseError
from django.core.exceptions import (
    ObjectDoesNotExist,
)  # TODO: replace with custom exception
from django.shortcuts import render
from django.utils import timezone
from .services.get_bikes import (
    fetch_all_pages,
    extract_data_from_page,
    parse_product_data,
)
from .models import SpecializedBike


# Create your views here.
def scrape_specialized(request):
    # try:
    #     pages = await fetch_all_pages()
    #     dfs = []
    #     for page in pages:
    #         json_data = extract_data_from_page(page)
    #         if json_data is not None:
    #             df = parse_product_data(json_data)
    #             if df is not None:
    #                 dfs.append(df)
    #     if len(dfs) > 0:
    #         df = pd.concat(dfs)
    #         df = df.sort_values(by="price", ascending=False).reset_index(drop=True)
    #         # bikes_data is a list of python dictionaries
    #         # dictionary keys are: 'name', 'size', 'class', 'type', 'subtype', 'price'
    #         bikes_data = df.to_dict(orient="records")
    #         for bike in bikes_data:
    #             name = bike.get("name")
    #             bike_already_exists = await sync_to_async(
    #                 SpecializedBike.objects.filter(name=name).exists
    #             )()
    #             if not bike_already_exists:
    #                 await sync_to_async(SpecializedBike.objects.create)(**bike)
    #             else:
    #                 saved_bike = await sync_to_async(
    #                     SpecializedBike.objects.filter(name=name)
    #                     .order_by("-created_at")
    #                     .first
    #                 )()
    #                 current_time = timezone.now()
    #                 bike_saved_time = saved_bike.created_at
    #                 delta = current_time - bike_saved_time
    #                 delta_in_hours = delta.total_seconds() / 3600
    #                 print(
    #                     f"{name} already exists in the database. Time since last scrape: {delta_in_hours} hours"
    #                 )
    #                 if delta_in_hours > 24:
    #                     print("re-scraping for new data")
    #                     await sync_to_async(SpecializedBike.objects.create)(**bike)
    #     else:
    #         raise Exception("No data found in the pages")

    # except Exception as e:
    #     print(f"Error: {str(e)}")  # TODO: add logging in settings.py
    #     raise ObjectDoesNotExist("Error fetching data from Specialized website")
    try:
        bikes_data = SpecializedBike.objects.all()
    except Exception as e:
        print(f"Error: {str(e)}")  # TODO: add logging in settings.py
        raise DatabaseError("Can't fetch specialized bikes")
        

    return render(
        request, "scraper/scrape_specialized.html", context={"bikes": bikes_data}
    )


def home(request):
    return render(request, "scraper/home.html")
