export const style = {
  version: 8,
  name: "PLAN IGN",
  metadata: { "maputnik:renderer": "mbgljs" },
  sources: {
    plan_ign: {
      type: "vector",
      tiles: ["https://data.geopf.fr/tms/1.0.0/PLAN.IGN/{z}/{x}/{y}.pbf"],
    },
    parc_elec: {
      type: "vector",
      url: import.meta.env.VITE_TILES_SERVER_URL,
    },
  },
  glyphs:
    "https://data.geopf.fr/annexes/ressources/vectorTiles/fonts/{fontstack}/{range}.pbf",
  sprite:
    "https://data.geopf.fr/annexes/ressources/vectorTiles/styles/PLAN.IGN/sprite/PlanIgn-Gris",
  transition: { duration: 300, delay: 0 },
  layers: [],
  id: "6lc64jimd",
};
