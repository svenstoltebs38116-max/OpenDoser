export class ODForm extends HTMLElement {

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this._fields = [];

        this.render();

    }

    connectedCallback() {
        this.render();
    }

    set fields(value) {

        this._fields = value ?? [];

        this.render();

    }

    get values() {

        const values = {};

        this._fields.forEach(field => {

            const element =
                this.shadowRoot.getElementById(field.id);

            if (!element) {
                return;
            }

            switch (field.type) {

                case "number":
                    values[field.id] = Number(element.value);
                    break;

                case "checkbox":
                    values[field.id] = element.checked;
                    break;

                default:
                    values[field.id] = element.value;

            }

        });

        return values;

    }

    renderField(field) {

        switch (field.type) {

            case "number":

                return `
                    <input
                        id="${field.id}"
                        type="number"
                        value="${field.value ?? ""}">
                `;

            case "checkbox":

                return `
                    <input
                        id="${field.id}"
                        type="checkbox"
                        ${field.value ? "checked" : ""}>
                `;

            case "select":

                return `
                    <select id="${field.id}">
                        ${(field.options ?? []).map(option => `
                            <option
                                value="${option.value}"
                                ${option.value === field.value ? "selected" : ""}>
                                ${option.label}
                            </option>
                        `).join("")}
                    </select>
                `;

            default:

                return `
                    <input
                        id="${field.id}"
                        type="text"
                        value="${field.value ?? ""}">
                `;

        }

    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display: block;
                }

                form {

                    display: flex;
                    flex-direction: column;
                    gap: 18px;

                }

                label {

                    display: flex;
                    flex-direction: column;
                    gap: 6px;

                    font-size: 14px;

                }

                input,
                select {

                    padding: 10px 12px;

                    border-radius: 8px;

                    border: 1px solid var(--divider-color);

                    background: var(--card-background-color);

                    color: var(--primary-text-color);

                    font: inherit;

                    box-sizing: border-box;

                    width: 100%;

                }

                input[type="checkbox"] {

                    width: auto;

                    align-self: flex-start;

                }

            </style>

            <form>

                ${this._fields.map(field => `

                    <label>

                        ${field.label}

                        ${this.renderField(field)}

                    </label>

                `).join("")}

            </form>
        `;

    }

}

customElements.define(
    "od-form",
    ODForm,
);