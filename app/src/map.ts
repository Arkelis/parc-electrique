import { Map } from "maplibre-gl";
import planIgn from './map-styles/plan-ign.json'
import ignLayers from './map-styles/ign-layers.json'
import powerPlantsLayers from './map-styles/power-plants-layers.json'

import "./style.css";

const style = planIgn
planIgn.layers = [...ignLayers, ...powerPlantsLayers]

const map = new Map({
  container: "map", // container id
 // style: "https://demotiles.maplibre.org/style.json",
  style,
  center: [2.2, 47.2],
  zoom: 5, // starting zoom
});

// map.on('load', () => {
//   map.setLayoutProperty('power_plants_name', 'text-field', [
//       'format',
//       ['get', 'osm_id']
//   ]);
// });
