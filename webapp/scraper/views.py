import logging

from django.db import DatabaseError
from django.shortcuts import render
from django.utils import timezone
from .services.get_bikes import (
    fetch_all_pages,
    extract_data_from_page,
    parse_product_data,
    save_bikes_to_database
)
from .models import SpecializedBike
from core.models import OutgoingRequest
from core.time_utils import total_seconds_since
logger = logging.getLogger("scraper")

# Create your views here.
def specialized_bikes(request):
    # try:
    #     last_request = OutgoingRequest.objects.latest("created_at")
    #     seconds_since_last_request = total_seconds_since(last_request.created_at)
    #     print(seconds_since_last_request)
    #     if seconds_since_last_request > BIKE_UPDATE_INTERVAL_SECONDS:
    #         pages = fetch_all_pages()
    #         all_bikes = []
    #         for page in pages:
    #             json_data = extract_data_from_page(page)
    #             if json_data is not None:
    #                 bikes_on_page = parse_product_data(json_data)
    #                 if bikes_on_page is not None:
    #                     all_bikes.extend(bikes_on_page)
    #             save_bikes_to_database(all_bikes)
    # except Exception as e:
    #     logger.error(f"Error: {str(e)}")  # TODO: add logging in settings.py
    #     raise DatabaseError("Can't fetch specialized bikes")
        
    bikes_data = SpecializedBike.objects.all().order_by("-price")
    return render(
        request, "scraper/scrape_specialized.html", context={"bikes": bikes_data}
    )


def home(request):
    return render(request, "scraper/home.html")
