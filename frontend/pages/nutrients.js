import BasePage from "./base_page.js";

export default class NutrientsPage extends BasePage {

    get pageId() {
        return "nutrients";
    }

    get pageTitle() {
        return "Nutrients";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Add Nutrient",
                action: () => this.openCreateDialog(),
            },
        ];
    }

    async renderPage() {

        return `
            <od-card title="Nutrients">

                <od-table id="table"></od-table>

            </od-card>
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
                key: "actions",
                label: "",
            },
        ];

        table.rows = (this.app.system?.nutrients ?? []).map((nutrient) => ({

            ...nutrient,

            actions: [
                {
                    icon: "mdi:pencil",
                    title: "Edit",
                    action: () => this.openEditDialog(nutrient),
                },
                {
                    icon: "mdi:delete",
                    title: "Delete",
                    action: () => this.deleteNutrient(nutrient),
                },
            ],

        }));

    }

    openCreateDialog() {

        this.openNutrientDialog();

    }

    openEditDialog(nutrient) {

        this.openNutrientDialog(nutrient);

    }

    openNutrientDialog(nutrient = null) {

        const form = document.createElement("od-form");

        form.fields = [
            {
                id: "id",
                label: "ID",
                value: nutrient?.id ?? "",
            },
            {
                id: "name",
                label: "Name",
                value: nutrient?.name ?? "",
            },
        ];

        this.dialog.open({

            title: nutrient ? "Edit Nutrient" : "New Nutrient",

            content: form,

            actions: [
                {
                    label: "Cancel",
                },
                {
                    label: "Save",

                    primary: true,

                    action: async () => {

                        if (nutrient) {

                            await this.app.update(
                                "nutrient",
                                form.values,
                            );

                        } else {

                            await this.app.create(
                                "nutrient",
                                form.values,
                            );

                        }

                        this.refresh();

                    },

                },
            ],

        });

    }

    async deleteNutrient(nutrient) {

        if (!confirm(`Delete "${nutrient.name}"?`)) {
            return;
        }

        await this.app.delete(
            "nutrient",
            nutrient.id,
        );

        this.refresh();

    }

}

customElements.define(
    "od-page-nutrients",
    NutrientsPage,
);