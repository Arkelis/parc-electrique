import { Map } from "maplibre-gl";
import style from './map-styles/style.json'
import ignLayers from './map-styles/layer-ign.json'
import { nuclearLayers } from './map-styles/layer-nuclear'

import "./style.css";

style.layers = ignLayers;

const map = new Map({
  container: "map", // container id
  // style: "https://demotiles.maplibre.org/style.json",
  style,
  center: [3, 47.2],
  zoom: 5, // starting zoom
  antialias: true
});

map.on("load", () => {
  map.loadImage("http://localhost:5173/sprite/atom.png", (_, image) => {
    if (!image) return;
    map.addImage("atom", image);
  });

  nuclearLayers.forEach(layer => map.addLayer(layer))
});

map.on("click", "power_plants_area", (element) => {
  if (element.features === undefined) return;
  const properties = element.features[0].properties;
  console.log(properties);
  const plantClickedEvent = new CustomEvent("plantClicked", {
    detail: properties,
  });
  document.querySelector("body")?.dispatchEvent(plantClickedEvent);
});

document
  .querySelector("body")
  ?.addEventListener("plantClicked", (event) => console.log(event));
