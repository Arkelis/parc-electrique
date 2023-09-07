import type { Component } from "solid-js";

import "./style.css";

const Sidebar: Component = () => {
  return (
    <div class='p-4'>
      <h1 class="font-light text-4xl mb-4">Géowatt</h1>
      <p class='text-sm'>Cette carte interactive permet de visualiser l'ensemble des centrales électriques en France métropolitaine, ainsi que leur production en temps réel.</p>
      <nav>
        <button>Production nucléaire</button>
      </nav>
    </div>
  );
};

export default Sidebar;
