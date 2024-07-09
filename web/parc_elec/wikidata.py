from django.core.cache import cache
import requests


WIKIDATA_API_ENDPOINT = "https://www.wikidata.org/w/rest.php/wikibase/v0/entities/items/{}/statements?property=P8645"
USER_AGENT = (
    "parc-elec/0.0 "
    "(https://pycolore.fr; guillaume.fayard@pycolore.fr) "
    "Python/{}.{}"
)


def _get_eic_from_payload(payload: dict):
    return payload.get("value", {}).get("content")


def _get_results_from_wikidata(entity_id: str):
    wikidata_response = requests.get(
        url=WIKIDATA_API_ENDPOINT.format(entity_id), headers={"User-Agent": USER_AGENT}
    )
    json_response = wikidata_response.json()

    if not (code_payload_list := json_response.get("P8645")):
        return []

    return [
        code
        for payload in code_payload_list
        if (code := payload.get("value", {}).get("content")) is not None
    ]


def fetch_eic_identifiers(entity_id: str):
    """Retrieve from Wikidata eic identifiers of the given element.

    entity_id is the Wikidata id of the element.
    Return a list of str.
    """
    cache_key = f"wd:{entity_id}:eic"
    if cached_value := cache.get(cache_key):
        return cached_value

    eic_identifiers = _get_results_from_wikidata(entity_id)
    cache.set(cache_key, eic_identifiers, 3600 * 24)
    return eic_identifiers
