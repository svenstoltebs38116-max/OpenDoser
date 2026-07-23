import "../components/od-sidebar.js";
import "../components/od-toolbar.js";
import "../components/od-card.js";
import "../components/od-dialog.js";
import "../components/od-form.js";
import "../components/od-table.js";

export default class BasePage extends HTMLElement {

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this.app = null;

    }

    get pageId() {
        return "";
    }

    get pageTitle() {
        return "";
    }

    get toolbarActions() {
        return [];
    }

    async connectedCallback() {

        await this.refresh();

    }

    async refresh() {

        if (!this.app) {
            return;
        }

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display: block;
                    height: 100%;
                }

                .layout {
                    display: grid;
                    grid-template-columns: 250px 1fr;
                    height: 100%;
                }

                .main {
                    display: flex;
                    flex-direction: column;
                    overflow: hidden;
                }

                .page {
                    flex: 1;
                    overflow: auto;
                    padding: 24px;
                    background: var(--primary-background-color);
                }

            </style>

            <div class="layout">

                <od-sidebar id="sidebar"></od-sidebar>

                <div class="main">

                    <od-toolbar id="toolbar"></od-toolbar>

                    <div
                        id="page"
                        class="page">

                        ${await this.renderPage()}

                    </div>

                </div>

            </div>

            <od-dialog id="dialog"></od-dialog>
        `;

        const sidebar =
            this.shadowRoot.getElementById("sidebar");

        sidebar.items = [
            {
                id: "dashboard",
                title: "Dashboard",
            },
            {
                id: "pumps",
                title: "Pumpen",
            },
            {
                id: "tanks",
                title: "Tanks",
            },
            {
                id: "nutrients",
                title: "Nährstoffe",
            },
            {
                id: "recipes",
                title: "Rezepte",
            },
            {
                id: "feed_programs",
                title: "Düngeprogramme",
            },
            {
                id: "settings",
                title: "Einstellungen",
            },
        ];

        sidebar.selected = this.pageId;

        sidebar.onNavigate = (page) => {

            this.app.navigate(page);

        };

        const toolbar =
            this.shadowRoot.getElementById("toolbar");

        toolbar.title = this.pageTitle;
        toolbar.actions = this.toolbarActions;

        if (this.pageRendered) {
            await this.pageRendered();
        }

    }

    async renderPage() {

        return "";

    }

    get dialog() {

        return this.shadowRoot.getElementById(
            "dialog",
        );

    }

}