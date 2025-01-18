import os
from datetime import datetime, timedelta
from loguru import logger
import requests

API_KEY = os.getenv("PARC_ELEC_FR_ODRE_API_KEY")


def fetch_eco2mix_national():
    logger.debug("Fetching eco2mix national")

    response = requests.get(
        f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-national-tr/records?{_query()}",
        headers={"Authorization": f"Apikey {API_KEY}"},
    )

    logger.debug(f"Response status: {response.status_code}")
    if response.status_code != 200:
        return

    logger.debug("eco2mix national fetched")

    return response.json()


def fetch_eco2mix_regional():
    logger.debug("Fetching eco2mix regional")

    response = requests.get(
        f"https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/eco2mix-regional-tr/records?{_query()}",
        headers={"Authorization": f"Apikey {API_KEY}"},
    )

    logger.debug(f"Response status: {response.status_code}")
    if response.status_code != 200:
        return

    logger.debug("eco2mix regional fetched")

    return response.json()


def _query():
    return (
        f"where=consommation IS NOT NULL AND date_heure > '{_a_day_ago().isoformat()}' AND heure like '%:00'"
        "&order_by=date_heure ASC"
        "&limit=-1"
    )


def _a_day_ago():
    return datetime.now() - timedelta(hours=8)
