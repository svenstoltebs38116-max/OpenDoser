import BasePage from "./base_page.js";

export default class TanksPage extends BasePage {

    get pageId() {
        return "tanks";
    }

    get pageTitle() {
        return "Tanks";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Add Tank",
                action: () => this.openCreateDialog(),
            },
        ];
    }

    async renderPage() {

        return `
            <od-card title="Tanks">

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
                key: "volume",
                label: "Volume (L)",
            },
            {
                key: "actions",
                label: "",
            },
        ];

        table.rows = (this.app.system?.tanks ?? []).map((tank) => ({

            ...tank,

            actions: [
                {
                    icon: "mdi:pencil",
                    title: "Edit",
                    action: () => this.openEditDialog(tank),
                },
                {
                    icon: "mdi:delete",
                    title: "Delete",
                    action: () => this.deleteTank(tank),
                },
            ],

        }));

    }

    openCreateDialog() {

        this.openTankDialog();

    }

    openEditDialog(tank) {

        this.openTankDialog(tank);

    }

    openTankDialog(tank = null) {

        const form = document.createElement("od-form");

        form.fields = [
            {
                id: "id",
                label: "ID",
                value: tank?.id ?? "",
            },
            {
                id: "name",
                label: "Name",
                value: tank?.name ?? "",
            },
            {
                id: "volume",
                label: "Volume (L)",
                type: "number",
                value: tank?.volume ?? 0,
            },
        ];

        this.dialog.open({

            title: tank ? "Edit Tank" : "New Tank",

            content: form,

            actions: [
                {
                    label: "Cancel",
                },
                {
                    label: "Save",
                    primary: true,

                    action: async () => {

                        if (tank) {

                            await this.app.update(
                                "tank",
                                form.values,
                            );

                        } else {

                            await this.app.create(
                                "tank",
                                form.values,
                            );

                        }

                        this.refresh();

                    },
                },
            ],
        });

    }

    async deleteTank(tank) {

        if (!confirm(`Delete "${tank.name}"?`)) {
            return;
        }

        await this.app.delete(
            "tank",
            tank.id,
        );

        this.refresh();

    }

}

customElements.define(
    "od-page-tanks",
    TanksPage,
);