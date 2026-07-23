import BasePage from "./base_page.js";

export default class CrudPage extends BasePage {

    get objectType() {
        throw new Error("objectType must be implemented");
    }

    get pageTitle() {
        return "CRUD";
    }

    get columns() {
        return [];
    }

    get fields() {
        return [];
    }

    get items() {
        return this.app.system?.[`${this.objectType}s`] ?? [];
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Neu",
                action: () => this.createItem(),
            },
        ];
    }

    async renderPage() {

        return `
            <od-table id="table"></od-table>
            <od-dialog id="dialog"></od-dialog>
        `;

    }

    async pageRendered() {

        const table = this.shadowRoot.getElementById("table");

        table.columns = this.columns;
        table.rows = this.items;

        table.onEdit = (row) => this.editItem(row);
        table.onDelete = (row) => this.deleteItem(row);

    }

    async createItem() {

        const dialog = this.shadowRoot.getElementById("dialog");

        const values = await dialog.open(
            `Neue(r) ${this.pageTitle}`,
            structuredClone(this.fields),
        );

        if (!values) {
            return;
        }

        await this.app.create(
            this.objectType,
            values,
        );

        await this.refresh();

    }

    async editItem(item) {

        const dialog = this.shadowRoot.getElementById("dialog");

        const fields = structuredClone(this.fields);

        fields.forEach(field => {

            field.value = item[field.id];

        });

        const values = await dialog.open(
            `${this.pageTitle} bearbeiten`,
            fields,
        );

        if (!values) {
            return;
        }

        values.id = item.id;

        await this.app.update(
            this.objectType,
            values,
        );

        await this.refresh();

    }

    async deleteItem(item) {

        if (!confirm(`"${item.name}" wirklich löschen?`)) {
            return;
        }

        await this.app.delete(
            this.objectType,
            item.id,
        );

        await this.refresh();

    }

}