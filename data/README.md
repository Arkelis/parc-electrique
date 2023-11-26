# Import des données pour Géowatt

## Données cartographiques sur les centrales

Dans le dossier `osm` se trouve le script pour importer les données d'OpenStreetMap.
Pour lancer l'import il faut avoir téléchargé un export de la France métropolitaine
depuis OpenStreetMap.

Voir : http://download.openstreetmap.fr/extracts/europe/

Une fois l'export de la France est téléchargé, il doit être placé dans le dossier
`osm` et nommé `france.osm.pbf`.

Pour lancer l'extraction des données des centrales, lancer la commande depuis
la racine de ce dépôt :

```sh
sh bin/import-osm.sh
```

## Contours des régions

Dans le dossier `regions` se trouve le script pour importer les contours des régions. C'est utile pour rattacher chaque centrale à sa région. Il faut télécharger ici les données depuis le site osm13.openstreetmap.fr.

Voir : https://osm13.openstreetmap.fr/~cquest/openfla/export/

Une fois l'export téléchargé, il doit être décompressé et tous les fichiers copiés à plat dans `regions`.

Pour lancer l'import des contours de régions, lancer la commande depuis
la racine de ce dépôt :

```sh
sh bin/import-regions.sh
```