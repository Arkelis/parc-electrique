import json

import requests
from loguru import logger


def get_hydrau_stations():
    logger.debug("Fetching hydraulic stations")

    response = requests.get(
        'https://opendata.edf.fr/api/explore/v2.1/catalog/datasets/centrales-de-production-hydraulique-de-edf-sa/records?select=centrale,categorie_centrale,commune,departement,point_gps_wsg_84,puissance_installee,unite&lang=fr'
    )
    logger.debug("Access token fetched")

    with open('../edf_hydrau.json', 'w') as file:
        json.dump(response.json(), file, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    get_hydrau_stations()
