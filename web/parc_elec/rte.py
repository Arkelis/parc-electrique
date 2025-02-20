import os

from loguru import logger
import requests
from requests.adapters import HTTPAdapter, Retry
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv("PARC_ELEC_FR_RTE_CLIENT_ID")
CLIENT_SECRET = os.getenv("PARC_ELEC_FR_RTE_CLIENT_SECRET")


def _get_access_token(session):
    logger.debug("Fetching access token")

    assert CLIENT_ID is not None, "client id is not defined"
    assert CLIENT_SECRET is not None, "client secret is not defined"

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = session.post(
        "https://digital.iservices.rte-france.com/token/oauth/", auth=auth
    ).json()
    logger.debug("Access token fetched")

    return response["access_token"]


def _get_session():
    session = requests.Session()
    retries = Retry(total=10, backoff_factor=0.2, status_forcelist=[500, 502])
    session.mount(
        "https://digital.iservices.rte-france.com",
        adapter=HTTPAdapter(max_retries=retries),
    )

    return session



def fetch_current_production():
    logger.debug("Fetching production data")

    session = _get_session()
    token = _get_access_token(session)
    response = session.get(
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

    session = _get_session()
    token = _get_access_token(session)
    response = session.get(
        "https://digital.iservices.rte-france.com/open_api/generation_installed_capacities/v1/capacities_per_production_unit",
        headers={"Authorization": f"Bearer {token}"},
    )

    logger.debug(f"Response status: {response.status_code}")
    if response.status_code != 200:
        raise RuntimeError("Could not fetch installed capacity from RTE")

    logger.debug("Installed data fetched")

    return response.json()
