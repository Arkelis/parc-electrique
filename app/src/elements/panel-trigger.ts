import { LitElement } from "lit";
import { customElement } from "lit/decorators.js";

@customElement("parc-elec-panel-trigger")
export class ParcElecPanelTrigger extends LitElement {
  createRenderRoot() {
    return this;
  }

  connectedCallback() {
    this.addEventListener("click", () =>
      window.dispatchEvent(new Event("togglepanel"))
    );
  }
}
