import json
import re


def get_hydrau_production():
    with open('edf_hydrau.json', 'r', encoding='utf-8') as hydrau_stations, open('production.json', 'r', encoding='utf-8') as production:
        stations = json.load(hydrau_stations)['results']
        productions = json.load(production)['actual_generations_per_unit']

        for station in stations:
            for prod in productions:
                # remove digit from station name
                print('---')
                unit_name = re.sub(r'\d', '', prod['unit']['name']).upper()
                print(unit_name)

                if unit_name in station['centrale'] or unit_name in station['commune']:
                    print(unit_name, 'found')


if __name__ == '__main__':
    get_hydrau_production()