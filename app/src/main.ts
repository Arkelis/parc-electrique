import { Map } from "maplibre-gl";
import planIgn from './map-styles/plan-ign.json'
import ignLayers from './map-styles/ign_layers.json'
import "./style.css";

const style = planIgn
planIgn.layers = ignLayers

const map = new Map({
  container: "map", // container id
 // style: "https://demotiles.maplibre.org/style.json",
  style,
  center: [2.2, 46.2],
  zoom: 5, // starting zoom
});
