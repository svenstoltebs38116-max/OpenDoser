import CrudPage from "./crud_page.js";

export default class NutrientsPage extends CrudPage {

    get pageId() {
        return "nutrients";
    }

    get pageTitle() {
        return "Nährstoffe";
    }

    get objectType() {
        return "nutrient";
    }

    get columns() {
        return [
            {
                key: "id",
                label: "ID",
            },
            {
                key: "name",
                label: "Name",
            },
            {
                key: "tank_id",
                label: "Tank",
            },
            {
                key: "enabled",
                label: "Aktiv",
            },
        ];
    }

    get fields() {

        return [
            {
                id: "name",
                label: "Name",
                type: "text",
                required: true,
            },
            {
                id: "tank_id",
                label: "Tank",
                type: "select",
                options: (this.app.system?.tanks ?? []).map(tank => ({
                    value: tank.id,
                    label: tank.name,
                })),
                required: true,
            },
            {
                id: "enabled",
                label: "Aktiv",
                type: "checkbox",
                value: true,
            },
        ];

    }

}

customElements.define(
    "od-page-nutrients",
    NutrientsPage,
);