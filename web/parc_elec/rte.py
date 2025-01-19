import os

from loguru import logger
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv("PARC_ELEC_FR_RTE_CLIENT_ID")
CLIENT_SECRET = os.getenv("PARC_ELEC_FR_RTE_CLIENT_SECRET")


def _get_access_token():
    logger.debug("Fetching access token")

    assert CLIENT_ID is not None, "client id is not defined"
    assert CLIENT_SECRET is not None, "client secret is not defined"

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(
        "https://digital.iservices.rte-france.com/token/oauth/", auth=auth
    ).json()
    logger.debug("Access token fetched")

    return response["access_token"]


def fetch_current_production_mix():
    logger.debug("Fetching mix")

    token = _get_access_token()
    response = requests.get(
        "https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_production_type",
        headers={"Authorization": f"Bearer {token}"},
    )

    logger.debug(f"Response status: {response.status_code}")
    if response.status_code != 200:
        logger.error("Could not fetch mix data")
        raise RuntimeError("Could not fetch mix from RTE")

    logger.debug("Mix fetched")

    return response.json()


def fetch_current_production():
    logger.debug("Fetching production data")

    token = _get_access_token()
    s = requests.Session()
    retries = Retry(total=10, backoff_factor=0.5, status_forcelist=[500, 502])
    s.mount(
        "https://digital.iservices.rte-france.com",
        adapter=HTTPAdapter(max_retries=retries),
    )
    response = s.get(
        "https://digital.iservices.rte-france.com/open_api/actual_generation/v1/actual_generations_per_unit",
        headers={"Authorization": f"Bearer {token}"},
    )

    logger.debug("Response status:", response.status_code)
    if response.status_code != 200:
        raise RuntimeError("Could not fetch production from RTE")

    logger.debug("Production data fetched")

    return response.json()


def fetch_current_installed_capacity():
    logger.debug("Fetching installed data")

    token = _get_access_token()
    s = requests.Session()
    retries = Retry(total=10, backoff_factor=0.5, status_forcelist=[500, 502])
    s.mount(
        "https://digital.iservices.rte-france.com", adapter=HTTPAdapter(max_retries=retries)
    )
    response = s.get(
        "https://digital.iservices.rte-france.com/open_api/generation_installed_capacities/v1/capacities_per_production_unit",
        headers={"Authorization": f"Bearer {token}"},
    )

    logger.debug(f"Response status: {response.status_code}")
    if response.status_code != 200:
        raise RuntimeError("Could not fetch installed capacity from RTE")

    logger.debug("Installed data fetched")

    return response.json()
