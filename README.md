# Parc électrique français (Géowatt)

<img width="1512" alt="image" src="https://github.com/user-attachments/assets/491992d2-915f-43af-a582-9084c6173b82" />

Ce dépôt contient le code de Géowatt, une carte interactive permettant de visualiser
les centales électriques en France ainsi que leur production. Il est structuré en
plusieurs parties :

- `data` : la récupération des données géographiques et énergétiques
- `map` : la génération de la carte
- `app` : le site web pour visualiser les données

## Sources de données

- Fond de carte : tuiles vectorielles issues des [Géoservices IGN](https://geoservices.ign.fr/services-web-essentiels)
- Données géographiques sur les centrales électriques : [OpenStreetMap](https://www.openstreetmap.org/), [Wikidata](https://www.wikidata.org)
- Données de production électrique : RTE

## Icones

Les icônes utilisées proviennent de la bibliothèque [OpenMoji](https://openmoji.org/)
