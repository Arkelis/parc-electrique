import json

import requests
from loguru import logger

def get_stations_from_osm():
    """This function performs the following query to the Overpass API

    [out:json]
    [timeout:25]
    ;
    area(3602202162)->.searchArea; // France
    (
      node
        ["plant:source"~"(nuclear|oil|coal|hydro|gas|biomass)"]
        (area.searchArea);
      way
        ["plant:source"~"(nuclear|oil|coal|hydro|gas|biomass)"]
        (area.searchArea);
      relation
        ["plant:source"~"(nuclear|oil|coal|hydro|gas|biomass)"]
        (area.searchArea);
    );
    out;
    >;
    out skel qt;
    """
    logger.debug("Fetching stations from OSM")
    response = requests.get('https://overpass-api.de/api/interpreter?data=%2F*%0AThis%20has%20been%20generated%20by%20the%20overpass-turbo%20wizard.%0AThe%20original%20search%20was%3A%0A%E2%80%9C%22plant%3Asource%22~%22%28nuclear%7Coil%7Ccoal%7Chydro%7Cgas%7Cbiomass%29%22%20in%20France%E2%80%9D%0A*%2F%0A%5Bout%3Ajson%5D%5Btimeout%3A25%5D%3B%0A%2F%2F%20fetch%20area%20%E2%80%9CFrance%E2%80%9D%20to%20search%20in%0Aarea%28id%3A3602202162%29-%3E.searchArea%3B%0A%2F%2F%20gather%20results%0A%28%0A%20%20%2F%2F%20query%20part%20for%3A%20%E2%80%9C%22plant%3Asource%22~%2F%28nuclear%7Coil%7Ccoal%7Chydro%7Cgas%7Cbiomass%29%2F%E2%80%9D%0A%20%20node%5B%22plant%3Asource%22~%22%28nuclear%7Coil%7Ccoal%7Chydro%7Cgas%7Cbiomass%29%22%5D%28area.searchArea%29%3B%0A%20%20way%5B%22plant%3Asource%22~%22%28nuclear%7Coil%7Ccoal%7Chydro%7Cgas%7Cbiomass%29%22%5D%28area.searchArea%29%3B%0A%20%20relation%5B%22plant%3Asource%22~%22%28nuclear%7Coil%7Ccoal%7Chydro%7Cgas%7Cbiomass%29%22%5D%28area.searchArea%29%3B%0A%29%3B%0A%2F%2F%20print%20results%0Aout%20body%3B%0A%3E%3B%0Aout%20skel%20qt%3B')

    logger.debug("Fetched from OSM")
    with open('elec-plants.json', 'w') as f:
        json.dump(response.json(), f, indent=2, ensure_ascii=False)

    logger.debug('Stations from OSM written locally')


if __name__ == '__main__':
    get_stations_from_osm()

