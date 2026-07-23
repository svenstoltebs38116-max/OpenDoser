export class ODToolbar extends HTMLElement {

    constructor() {
        super();

        this.attachShadow({
            mode: "open",
        });

        this._title = "";
        this._actions = [];
    }

    set title(value) {
        this._title = value ?? "";
        this.render();
    }

    set actions(value) {
        this._actions = value ?? [];
        this.render();
    }

    connectedCallback() {
        this.render();
    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    height: 64px;
                    padding: 0 24px;
                    background: var(--card-background-color);
                    border-bottom: 1px solid var(--divider-color);
                    box-sizing: border-box;
                }

                .title {
                    font-size: 24px;
                    font-weight: 600;
                }

                .actions {
                    display: flex;
                    gap: 12px;
                }

                button {
                    all: unset;
                    cursor: pointer;
                    padding: 10px 18px;
                    border-radius: 8px;
                    background: var(--primary-color);
                    color: white;
                    font-weight: 600;
                    transition: opacity .2s;
                }

                button:hover {
                    opacity: .85;
                }

            </style>

            <div class="title">
                ${this._title}
            </div>

            <div class="actions">
                ${this._actions.map((action, index) => `
                    <button data-index="${index}">
                        ${action.label}
                    </button>
                `).join("")}
            </div>
        `;

        this.shadowRoot
            .querySelectorAll("button")
            .forEach(button => {

                button.onclick = () => {

                    const action =
                        this._actions[
                            Number(button.dataset.index)
                        ];

                    if (action?.handler) {
                        action.handler();
                    }

                };

            });

    }

}

customElements.define(
    "od-toolbar",
    ODToolbar,
);