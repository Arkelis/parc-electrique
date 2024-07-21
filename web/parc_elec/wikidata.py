from collections import namedtuple
from collections import defaultdict
import sys

from django.core.cache import cache
from SPARQLWrapper import SPARQLWrapper, JSON


WIKIDATA_SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
WIKIDATA_SPARQL_QUERY = """
    SELECT ?eic ?item WHERE {{
    VALUES ?item {{ {wikidata_ids} }}
    OPTIONAL {{ ?item wdt:P8645 ?eic. }}
    }}
"""
USER_AGENT = (
    "parc-elec/0.0 "
    "(https://pycolore.fr; guillaume.fayard@pycolore.fr) "
    "Python/{}.{}"
)

EicTuple = namedtuple("EicTuple", ["qid", "eic"])


def _get_results_from_wikidata(wikidata_ids: list[str]):
    user_agent = USER_AGENT.format(sys.version_info[0], sys.version_info[1])
    formatted_ids = " ".join(f"wd:{qid}" for qid in wikidata_ids)

    sparql = SPARQLWrapper(WIKIDATA_SPARQL_ENDPOINT, agent=user_agent)
    sparql.setQuery(WIKIDATA_SPARQL_QUERY.format(wikidata_ids=formatted_ids))
    sparql.setReturnFormat(JSON)

    json_response = sparql.query().convert()

    return json_response["results"]["bindings"]


def _qid_from_url(url):
    return url.removeprefix("http://www.wikidata.org/entity/")


def _result_to_tuple(sparql_row):
    return EicTuple(
        _qid_from_url(sparql_row["item"]["value"]), sparql_row["eic"]["value"]
    )


def _tuples_to_dict(tuples):
    """Group by QID

    Take [(QID, EIC1), (QID, EIC2), ...]
    Return {QID: [EIC1, EIC2], ...}
    """
    result = defaultdict(list)
    for tuple in tuples:
        qid, eic = tuple
        result[qid].append(eic)

    return result


def fetch_eic_identifiers(wikidata_ids):
    """Retrieve from Wikidata EIC identifiers of the all elements.

    Take a list of wikidata ids (or QIDs)
    Return a dict:
    - keys are the qids
    - values are the lists of EIC.
    """
    sparql_results = _get_results_from_wikidata(wikidata_ids)
    plant_eic_tuples = [_result_to_tuple(row) for row in sparql_results]
    return _tuples_to_dict(plant_eic_tuples)
