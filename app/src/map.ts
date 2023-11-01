import { Map } from "maplibre-gl";
import style from "./map-styles/style.json";
import ignLayers from "./map-styles/layer-ign.json";
import { energyLayers } from "./map-styles/energy-layers";
import * as htmx from "htmx.org";

import "./style.css";

const icons = ["atom", "water", "fire", "wind", "sun", "electricity"];

style.layers = ignLayers;

const map = new Map({
  container: "map", // container id
  // style: "https://demotiles.maplibre.org/style.json",
  style,
  center: [5, 47.2],
  zoom: 5, // starting zoom
  antialias: true,
});

map.on("load", () => {
  icons.forEach((iconName) =>
    map.loadImage(
      `http://localhost:5173/sprite/${iconName}.png`,
      (_, image) => {
        if (!image) return;
        map.addImage(iconName, image);
      }
    )
  );

  energyLayers().forEach((layer) => map.addLayer(layer));

  map.on("click", "power_plants_icon", (element) => {
    if (element.features === undefined) return;
    const properties = element.features[0].properties;
    console.log(properties);
    const plantUrl = `/plant/${properties.gid}`
    htmx.ajax("get", plantUrl, "#panel");
    history.pushState(null, '', plantUrl)
  });

  map.on("mouseenter", "power_plants_icon", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseleave", "power_plants_icon", () => {
    map.getCanvas().style.cursor = "grab";
  });
});

window.addEventListener('popstate', function (ev) {
  htmx.ajax("get", document.location.href, "#panel");
});

