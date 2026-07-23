import BasePage from "./base_page.js";

export default class FeedProgramsPage extends BasePage {

    get pageId() {
        return "feed_programs";
    }

    get pageTitle() {
        return "Feed Programs";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Add Program",
                action: () => this.openCreateDialog(),
            },
        ];
    }

    async renderPage() {

        return `
            <od-card title="Feed Programs">

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

        table.rows = (this.app.system?.feed_programs ?? []).map((program) => ({

            ...program,

            actions: [
                {
                    icon: "mdi:pencil",
                    title: "Edit",
                    action: () => this.openEditDialog(program),
                },
                {
                    icon: "mdi:delete",
                    title: "Delete",
                    action: () => this.deleteProgram(program),
                },
            ],

        }));

    }

    openCreateDialog() {

        this.openProgramDialog();

    }

    openEditDialog(program) {

        this.openProgramDialog(program);

    }

    openProgramDialog(program = null) {

        const form = document.createElement("od-form");

        form.fields = [
            {
                id: "id",
                label: "ID",
                value: program?.id ?? "",
            },
            {
                id: "name",
                label: "Name",
                value: program?.name ?? "",
            },
        ];

        this.dialog.open({

            title: program ? "Edit Feed Program" : "New Feed Program",

            content: form,

            actions: [
                {
                    label: "Cancel",
                },
                {
                    label: "Save",

                    primary: true,

                    action: async () => {

                        if (program) {

                            await this.app.update(
                                "feed_program",
                                form.values,
                            );

                        } else {

                            await this.app.create(
                                "feed_program",
                                form.values,
                            );

                        }

                        this.refresh();

                    },

                },
            ],

        });

    }

    async deleteProgram(program) {

        if (!confirm(`Delete "${program.name}"?`)) {
            return;
        }

        await this.app.delete(
            "feed_program",
            program.id,
        );

        this.refresh();

    }

}

customElements.define(
    "od-page-feed-programs",
    FeedProgramsPage,
);