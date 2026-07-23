import CrudPage from "./crud_page.js";

export default class TanksPage extends CrudPage {

    get pageId() {
        return "tanks";
    }

    get pageTitle() {
        return "Tanks";
    }

    get objectType() {
        return "tank";
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
                key: "capacity",
                label: "Volumen (ml)",
            },
            {
                key: "current_level",
                label: "Füllstand (ml)",
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
                id: "capacity",
                label: "Volumen (ml)",
                type: "number",
                required: true,
            },
            {
                id: "current_level",
                label: "Aktueller Füllstand (ml)",
                type: "number",
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
    "od-page-tanks",
    TanksPage,
);