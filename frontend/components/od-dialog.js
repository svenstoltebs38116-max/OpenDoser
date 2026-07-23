export class ODDialog extends HTMLElement {

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this._title = "";
        this._fields = [];
        this._resolve = null;

        this.render();
    }

    connectedCallback() {
        this.render();
    }

    async open(title, fields) {

        this._title = title;
        this._fields = fields;

        this.render();

        this.style.display = "flex";

        return new Promise(resolve => {
            this._resolve = resolve;
        });
    }

    close(result = null) {

        this.style.display = "none";

        if (this._resolve) {
            this._resolve(result);
            this._resolve = null;
        }

    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {

                    position: fixed;
                    inset: 0;

                    display: none;

                    align-items: center;
                    justify-content: center;

                    background: rgba(0,0,0,.45);

                    z-index: 9999;

                }

                .dialog {

                    width: 420px;
                    max-width: calc(100vw - 32px);

                    background: var(--card-background-color);

                    border-radius: 14px;

                    box-shadow: var(--ha-card-box-shadow, 0 6px 18px rgba(0,0,0,.25));

                    overflow: hidden;

                }

                .header {

                    padding: 20px 24px;

                    font-size: 20px;
                    font-weight: 600;

                    border-bottom: 1px solid var(--divider-color);

                }

                .content {

                    display: flex;
                    flex-direction: column;
                    gap: 18px;

                    padding: 24px;

                }

                label {

                    display: flex;
                    flex-direction: column;
                    gap: 6px;

                    font-size: 14px;

                }

                input {

                    padding: 10px 12px;

                    border: 1px solid var(--divider-color);

                    border-radius: 8px;

                    background: var(--primary-background-color);

                    color: var(--primary-text-color);

                    font: inherit;

                }

                .footer {

                    display: flex;
                    justify-content: flex-end;
                    gap: 12px;

                    padding: 18px 24px;

                    border-top: 1px solid var(--divider-color);

                }

                button {

                    border: none;

                    cursor: pointer;

                    padding: 10px 18px;

                    border-radius: 8px;

                    font: inherit;

                }

                .cancel {

                    background: var(--secondary-background-color);

                    color: var(--primary-text-color);

                }

                .ok {

                    background: var(--primary-color);

                    color: white;

                }

            </style>

            <div class="dialog">

                <div class="header">
                    ${this._title}
                </div>

                <div class="content">

                    ${this._fields.map(field => `

                        <label>

                            ${field.label}

                            <input
                                id="${field.id}"
                                value="${field.value ?? ""}"
                                type="${field.type ?? "text"}">

                        </label>

                    `).join("")}

                </div>

                <div class="footer">

                    <button class="cancel">
                        Abbrechen
                    </button>

                    <button class="ok">
                        OK
                    </button>

                </div>

            </div>
        `;

        this.shadowRoot
            .querySelector(".cancel")
            ?.addEventListener(
                "click",
                () => this.close(null),
            );

        this.shadowRoot
            .querySelector(".ok")
            ?.addEventListener(
                "click",
                () => {

                    const values = {};

                    this._fields.forEach(field => {

                        values[field.id] =
                            this.shadowRoot
                                .getElementById(field.id)
                                .value;

                    });

                    this.close(values);

                },
            );

    }

}

customElements.define(
    "od-dialog",
    ODDialog,
);