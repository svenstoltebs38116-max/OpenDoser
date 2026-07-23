import BasePage from "./base_page.js";

export default class RecipesPage extends BasePage {

    get pageId() {
        return "recipes";
    }

    get pageTitle() {
        return "Recipes";
    }

    get toolbarActions() {
        return [
            {
                icon: "mdi:plus",
                label: "Add Recipe",
                action: () => this.openCreateDialog(),
            },
        ];
    }

    async renderPage() {

        return `
            <od-card title="Recipes">

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

        table.rows = (this.app.system?.recipes ?? []).map((recipe) => ({

            ...recipe,

            actions: [
                {
                    icon: "mdi:pencil",
                    title: "Edit",
                    action: () => this.openEditDialog(recipe),
                },
                {
                    icon: "mdi:delete",
                    title: "Delete",
                    action: () => this.deleteRecipe(recipe),
                },
            ],

        }));

    }

    openCreateDialog() {

        this.openRecipeDialog();

    }

    openEditDialog(recipe) {

        this.openRecipeDialog(recipe);

    }

    openRecipeDialog(recipe = null) {

        const form = document.createElement("od-form");

        form.fields = [
            {
                id: "id",
                label: "ID",
                value: recipe?.id ?? "",
            },
            {
                id: "name",
                label: "Name",
                value: recipe?.name ?? "",
            },
        ];

        this.dialog.open({

            title: recipe ? "Edit Recipe" : "New Recipe",

            content: form,

            actions: [
                {
                    label: "Cancel",
                },
                {
                    label: "Save",

                    primary: true,

                    action: async () => {

                        if (recipe) {

                            await this.app.update(
                                "recipe",
                                form.values,
                            );

                        } else {

                            await this.app.create(
                                "recipe",
                                form.values,
                            );

                        }

                        this.refresh();

                    },

                },
            ],

        });

    }

    async deleteRecipe(recipe) {

        if (!confirm(`Delete "${recipe.name}"?`)) {
            return;
        }

        await this.app.delete(
            "recipe",
            recipe.id,
        );

        this.refresh();

    }

}

customElements.define(
    "od-page-recipes",
    RecipesPage,
);