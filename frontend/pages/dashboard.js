import BasePage from "./base_page.js";

export default class DashboardPage extends BasePage {

    get pageId() {
        return "dashboard";
    }

    get pageTitle() {
        return "Dashboard";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:refresh",
                label: "Refresh",
                action: async () => {

                    await this.app.load();

                    await this.refresh();

                },
            },
        ];
    }

    async renderPage() {

        const system = this.app.system ?? {};

        return `
            <div class="cards">

                <od-card
                    title="Pumpen">

                    <h1>${system.pumps?.length ?? 0}</h1>

                </od-card>

                <od-card
                    title="Tanks">

                    <h1>${system.tanks?.length ?? 0}</h1>

                </od-card>

                <od-card
                    title="Nährstoffe">

                    <h1>${system.nutrients?.length ?? 0}</h1>

                </od-card>

                <od-card
                    title="Rezepte">

                    <h1>${system.recipes?.length ?? 0}</h1>

                </od-card>

                <od-card
                    title="Programme">

                    <h1>${system.feed_programs?.length ?? 0}</h1>

                </od-card>

            </div>

            <style>

                .cards {

                    display: grid;

                    grid-template-columns: repeat(auto-fit,minmax(260px,1fr));

                    gap: 20px;

                }

                h1 {

                    margin: 20px 0;

                    text-align: center;

                    font-size: 42px;

                }

            </style>
        `;

    }

}

customElements.define(
    "od-page-dashboard",
    DashboardPage,
);