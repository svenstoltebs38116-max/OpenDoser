import BasePage from "./base_page.js";

export default class PumpsPage extends BasePage {

    get pageId() {
        return "pumps";
    }

    get pageTitle() {
        return "Pumpen";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Neu",
                action: () => this.createPump(),
            },
        ];
    }

    async renderPage() {

        const pumps = this.app.system?.pumps ?? [];

        return `
            <od-table id="table"></od-table>
        `;
    }

    async pageRendered() {

        const table = this.shadowRoot.getElementById("table");

        table.columns = [
            {
                key: "id",
                label: "ID",
            },
            {
                key: "name",
                label: "Name",
            },
            {
                key: "gpio_pin",
                label: "GPIO",
            },
            {
                key: "flow_rate",
                label: "ml/min",
            },
        ];

        table.rows = this.app.system?.pumps ?? [];

        table.onEdit = (row) => this.editPump(row);
        table.onDelete = (row) => this.deletePump(row);

    }

    async createPump() {

        // Dialog folgt im nächsten Schritt.
    }

    async editPump(pump) {

        // Dialog folgt im nächsten Schritt.
    }

    async deletePump(pump) {

        if (!confirm(`Pumpe "${pump.name}" löschen?`)) {
            return;
        }

        await this.app.delete(
            "pump",
            pump.id,
        );

        await this.refresh();

    }

}

customElements.define(
    "od-page-pumps",
    PumpsPage,
);