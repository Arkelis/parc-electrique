import "vite/modulepreload-polyfill";
import { Map } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { style } from "./map-styles/style";
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
  center: [3, 47.2],
  zoom: 5.5, // starting zoom
  antialias: true,
});

map.on("load", () => {
  icons.forEach((iconName) =>
    map.loadImage(
      `${import.meta.env.VITE_SPRITE_URL}/${iconName}.png`,
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
    const plantUrl = `/centrale/${properties.gid}`;
    htmx.ajax("get", plantUrl, "#panel").then(() => {
      history.pushState(null, "", plantUrl);
      window.dispatchEvent(new Event("togglepanel"));
    });
  });

  map.on("mouseenter", "power_plants_icon", () => {
    map.getCanvas().style.cursor = "pointer";
  });

  map.on("mouseleave", "power_plants_icon", () => {
    map.getCanvas().style.cursor = "grab";
  });
});

window.addEventListener("popstate", () => {
  htmx.ajax("get", document.location.href, "#panel");
});

window.addEventListener("togglepanel", () => {
  document.querySelector("#panel")?.classList.toggle("hidden");
});
