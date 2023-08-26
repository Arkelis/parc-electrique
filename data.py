import os
import json

from loguru import logger
import requests
from requests.auth import HTTPBasicAuth

CLIENT_ID = os.getenv("PARC_ELEC_FR_CLIENT_ID")
CLIENT_SECRET = os.getenv("PARC_ELEC_FR_CLIENT_SECRET")


def get_access_token():
    logger.debug("Fetching access token")

    assert CLIENT_ID is not None, "client id is not defined"
    assert CLIENT_SECRET is not None, "client secret is not defined"

    auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    response = requests.post(
        "https://digital.iservices.rte-france.com/token/oauth/", auth=auth
    ).json()
    logger.debug("Access token fetched")

    return response["access_token"]


def get_current_production():
    logger.debug("Fetching production data")

    token = get_access_token()
    response = requests.get(
        "https://digital.iservices.rte-france.com/open_api/actual_generation/v1/sandbox/actual_generations_per_unit",
        headers={"Authorization": f"Bearer {token}"},
    )

    logger.debug("Production data fetched")
    
    with open('production.json', 'w') as file:
        json.dump(response.json(), file, indent=2)

    logger.debug("Production data dumped")


if __name__ == "__main__":
    print(get_current_production())
