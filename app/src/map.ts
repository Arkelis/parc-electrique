import { Map } from "maplibre-gl";
import style from "./map-styles/style.json";
import ignLayers from "./map-styles/layer-ign.json";
import { nuclearLayers } from "./map-styles/layer-nuclear";
import { hydroLayers } from "./map-styles/layer-hydro";
import * as htmx from "htmx.org";

import "./style.css";

style.layers = ignLayers;
const icons = ["atom", "water"];

const map = new Map({
  container: "map", // container id
  // style: "https://demotiles.maplibre.org/style.json",
  style,
  center: [3, 47.2],
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

  hydroLayers.forEach((layer) => map.addLayer(layer));
  nuclearLayers.forEach((layer) => map.addLayer(layer));

  const nuclearLayerIcons = ["power_plants_icon"];

  nuclearLayerIcons.forEach((layerName) => {
    map.on("click", layerName, (element) => {
      if (element.features === undefined) return;
      const properties = element.features[0].properties;
      htmx.ajax("get", `/plant/${properties.gid}`, "#panel");
    });

    map.on("mouseenter", layerName, (element) => {
      console.log("ENTER", layerName);
      map.getCanvas().style.cursor = "pointer";
    });

    map.on("mouseleave", layerName, (element) => {
      console.log("LEAVE", layerName);
      map.getCanvas().style.cursor = "grab";
    });
  });
});
