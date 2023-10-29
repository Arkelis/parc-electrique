const energyStyles = {
  fossil: { icon: "fire", color: "#f1b31c" },
  nuclear: { icon: "atom", color: "#198EC8" },
  hydro: { icon: "water", color: "#198EC8" },
  wind: { icon: "wind", color: "#198EC8" },
  solar: { icon: "sun", color: "#f1b31c" },
};

const energyFamilies = {
  nuclear: 'nuclear',
  oil: 'fossil',
  gas: 'fossil',
  coal: 'fossil',
  hydro: 'hydro',
  tidal: 'hydro',
  wind: 'wind',
  solar: 'solar'
}

const colorExpression = () => {
  const base = ["match", ["get", "source"]]
  for (const energy in energyFamilies) {
    base.push(energy)
    base.push(energyStyles[energyFamilies[energy]].color)
  }
  base.push('#198EC8')
  return base
}

const iconExpression = () => {
  const base = ["match", ["get", "source"]]
  for (const energy in energyFamilies) {
    base.push(energy)
    base.push(energyStyles[energyFamilies[energy]].icon)
  }
  base.push('electricity')
  return base
}

export const energyLayers = () => {
  return [
    {
      id: `power_plants_area`,
      source: "parc_elec",
      "source-layer": "power_plants",
      type: "fill",
      minzoom: 10,
      paint: {
        "fill-antialias": true,
        "fill-color": colorExpression(),
        "fill-opacity": 0.5,
      },
    },
    {
      id: `power_plants_outline`,
      source: "parc_elec",
      "source-layer": "power_plants",
      type: "line",
      minzoom: 10,
      paint: {
        "line-width": 3,
        "line-color": colorExpression(),
      },
    },
    {
      id: `power_plants_circle`,
      source: "parc_elec",
      "source-layer": "power_plants_name",
      type: "circle",
      paint: {
        "circle-color": colorExpression(),
        "circle-radius": 3,
        "circle-opacity": 0.7,
      },
    },
    {
      id: `power_plants_icon`,
      source: "parc_elec",
      "source-layer": "power_plants_name",
      type: "symbol",
      filter: [
        "any",
        [">=", ["zoom"], 9],
        [">=", ["get", "output"], 1000000000],
      ],
      layout: {
        "icon-allow-overlap": true,
        "icon-image": iconExpression(),
        "icon-size": ["interpolate", ["linear"], ["zoom"], 7, 0.7, 18, 1],
      },
    },
    {
      id: `power_plants_name`,
      source: "parc_elec",
      "source-layer": "power_plants_name",
      type: "symbol",
      minzoom: 6.5,
      filter: [
        "any",
        [">=", ["get", "output"], 1000000000],
        [">=", ["zoom"], 9],
      ],
      layout: {
        "symbol-placement": "point",
        "text-field": "{name}",
        "text-offset": [0, 1.7],
        "text-size": ["interpolate", ["linear"], ["zoom"], 10, 11, 18, 13],
        "text-anchor": "top",
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
};
