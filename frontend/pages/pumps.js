import CrudPage from "./crud_page.js";

export default class PumpsPage extends CrudPage {

    get pageId() {
        return "pumps";
    }

    get pageTitle() {
        return "Pumpen";
    }

    get objectType() {
        return "pump";
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
                key: "gpio_pin",
                label: "GPIO",
            },
            {
                key: "flow_rate",
                label: "ml/min",
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
                id: "gpio_pin",
                label: "GPIO Pin",
                type: "number",
                required: true,
            },
            {
                id: "flow_rate",
                label: "Förderleistung (ml/min)",
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
    "od-page-pumps",
    PumpsPage,
);