import OpenDoserApp from "./app.js";

import DashboardPage from "./pages/dashboard.js";
import PumpsPage from "./pages/pumps.js";
import TanksPage from "./pages/tanks.js";
import NutrientsPage from "./pages/nutrients.js";
import RecipesPage from "./pages/recipes.js";
import FeedProgramsPage from "./pages/feed_programs.js";
import SettingsPage from "./pages/settings.js";

export class OpenDoserPanel extends HTMLElement {

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this._hass = null;
        this.app = null;

    }

    set hass(hass) {

        this._hass = hass;

        this.initialize();

    }

    get hass() {
        return this._hass;
    }

    async initialize() {

        if (!this._hass) {
            return;
        }

        if (!this.app) {

            this.app = new OpenDoserApp(this._hass);

            this.app.navigate = (page) => {
                this.navigate(page);
            };

            await this.app.load();

        }

        if (!this.currentPage) {
            this.navigate("dashboard");
        }

    }

    createPage(page) {

        switch (page) {

            case "dashboard":
                return new DashboardPage();

            case "pumps":
                return new PumpsPage();

            case "tanks":
                return new TanksPage();

            case "nutrients":
                return new NutrientsPage();

            case "recipes":
                return new RecipesPage();

            case "feed_programs":
                return new FeedProgramsPage();

            case "settings":
                return new SettingsPage();

            default:
                return new DashboardPage();

        }

    }

    async navigate(page) {

        this.currentPage = page;

        const element = this.createPage(page);

        element.app = this.app;

        this.shadowRoot.innerHTML = "";

        this.shadowRoot.appendChild(element);

    }

}

customElements.define(
    "opendoser-panel",
    OpenDoserPanel,
);