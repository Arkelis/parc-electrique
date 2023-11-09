type EnergyFamily = "fossil" | "nuclear" | "hydro" | "wind" | "solar";

const energyStyles: Record<EnergyFamily, { icon: string; color: string }> =
  JSON.parse(document.getElementById("energy-styles")?.innerText ?? "{}");

const energyFamilies: Record<string, EnergyFamily> = JSON.parse(
  document.getElementById("energy-families")?.innerText ?? "{}"
);

const colorExpression = () => {
  const base = ["match", ["get", "source"]];
  for (const energy in energyFamilies) {
    base.push(energy);
    base.push(energyStyles[energyFamilies[energy]].color);
  }
  base.push("#828282"); // default color
  return base;
};

const iconExpression = () => {
  const base = ["match", ["get", "source"]];
  for (const energy in energyFamilies) {
    base.push(energy);
    base.push(energyStyles[energyFamilies[energy]].icon);
  }
  base.push("electricity");
  return base;
};

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
      filter: [
        "all",
        ["<", ["zoom"], 10],
        ["<=", ["get", "output"], 1000000000],
      ],
      paint: {
        "circle-color": colorExpression(),
        "circle-radius": ["interpolate", ["linear"], ["zoom"], 7, 3, 10, 9],
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
        [">=", ["get", "output"], 1000000000],
        ["all", [">=", ["zoom"], 7], [">=", ["get", "output"], 100000000]],
        ["all", [">=", ["zoom"], 9], [">=", ["get", "output"], 10000000]],
        [">=", ["zoom"], 10],
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
        ["all", [">=", ["zoom"], 7], [">=", ["get", "output"], 100000000]],
        ["all", [">=", ["zoom"], 9], [">=", ["get", "output"], 10000000]],
        [">=", ["zoom"], 10],
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
