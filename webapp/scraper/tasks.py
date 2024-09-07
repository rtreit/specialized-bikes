import logging
import traceback

import pandas as pd
from celery import shared_task

from core.models import OutgoingRequest, Error
from core.time_utils import total_seconds_since
from .services.get_bikes import do_scrape

BIKE_UPDATE_INTERVAL_SECONDS = 3600
logger = logging.getLogger("scraper")


@shared_task
def testing_celery():
    try:
        logger.info("Celery's heart is beating: ..., da-dum, da-dum, da-dum,...")
        return "SUCCESS"
    except Exception as e:
        logger.error(f"Error in testing_celery: {e}")


@shared_task()
def scrape_specialized_bikes():
    try:
        last_request_exists = OutgoingRequest.objects.all().exists()
        if not last_request_exists:
            do_scrape()
            return
        last_request = OutgoingRequest.objects.latest("created_at")
        seconds_since_last_request = total_seconds_since(last_request.created_at)
        logger.info(f"seconds_since_last_request {seconds_since_last_request}")
        if seconds_since_last_request > BIKE_UPDATE_INTERVAL_SECONDS:
            do_scrape()
        logger.info(
            f"Skipping Scrape due to insufficient time passed {seconds_since_last_request}"
        )
    except Exception as e:
        error_message = f"Error rescraping bikes: {str(e)}"
        stack_trace = traceback.format_exc()
        logger.error(error_message)
        Error(message=error_message, stack_trace=stack_trace)
        raise Exception("Can't fetch specialized bikes")
