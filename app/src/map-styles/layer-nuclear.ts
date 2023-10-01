export const nuclearLayers = [
  {
    id: "power_plants_area",
    source: "parc_elec",
    "source-layer": "power_plants",
    type: "fill",
    minzoom: 10,
    paint: {
      "fill-antialias": true,
      "fill-color": "#198EC8",
      "fill-opacity": 0.5,
    },
  },
  {
    id: "power_plants_outline",
    source: "parc_elec",
    "source-layer": "power_plants",
    type: "line",
    minzoom: 10,
    paint: {
      "line-width": 3,
      "line-color": "#198EC8",
    },
  },
  {
    id: "power_plants_icon",
    source: "parc_elec",
    "source-layer": "power_plants_name",
    type: "symbol",
    layout: {
      "icon-allow-overlap": true,
      "icon-image": "atom",
      "icon-size": ["interpolate", ["linear"], ["zoom"], 7, 0.7, 18, 1],
    },
  },
  {
    id: "power_plants_name",
    source: "parc_elec",
    "source-layer": "power_plants_name",
    type: "symbol",
    minzoom: 7,
    layout: {
      "symbol-placement": "point",
      "text-field": "{name}",
      "text-offset": [0, 2.6],
      "text-size": ["interpolate", ["linear"], ["zoom"], 9, 10, 18, 15],
      "text-anchor": "center",
      "text-keep-upright": true,
      "text-max-angle": 45,
      "text-font": ["Source Sans Pro Bold Italic"],
    },
    paint: {
      "text-halo-color": "#fff",
      "text-halo-width": 1,
    },
  },
];
