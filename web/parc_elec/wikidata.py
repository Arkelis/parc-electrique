import sys

from django.core.cache import cache
from SPARQLWrapper import SPARQLWrapper, JSON


WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
USER_AGENT = (
    "parc-elec/0.0 "
    "(https://pycolore.fr; guillaume.fayard@pycolore.fr) "
    "Python/{}.{}"
)


def _get_results_from_wikidata(query: str):
    user_agent = USER_AGENT.format(sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def fetch_eic_identifiers(q: str):
    """Retrieve from Wikidata eic identifiers of the given element.

    q is the Wikidata id of the element.
    Return a list of str.
    """
    query = """
        SELECT ?code_d_identification_énergie WHERE {
        VALUES ?item { wd:Q1739407 }
        OPTIONAL { ?item wdt:P8645 ?code_d_identification_énergie. }
        }
    """
    cache_key = f'wd:{q}:eic'
    if cached_value := cache.get(cache_key):
        return cached_value

    wikidata_payload = _get_results_from_wikidata(query)
    identifiers = [binding['code_d_identification_énergie']['value']
                   for binding in wikidata_payload['results']['bindings']]
    cache.set(cache_key, identifiers, 3600 * 24)
    return identifiers
