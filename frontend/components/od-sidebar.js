export class ODSidebar extends HTMLElement {

    constructor() {
        super();

        this.attachShadow({
            mode: "open",
        });

        this._items = [];
        this._selected = "";
        this._callback = null;
    }

    set items(value) {
        this._items = value ?? [];
        this.render();
    }

    set selected(value) {
        this._selected = value;
        this.render();
    }

    set onNavigate(callback) {
        this._callback = callback;
    }

    connectedCallback() {
        this.render();
    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display: flex;
                    flex-direction: column;
                    width: 250px;
                    height: 100%;
                    background: var(--card-background-color);
                    border-right: 1px solid var(--divider-color);
                    box-sizing: border-box;
                }

                .title {
                    padding: 24px;
                    font-size: 24px;
                    font-weight: 600;
                    border-bottom: 1px solid var(--divider-color);
                }

                nav {
                    display: flex;
                    flex-direction: column;
                    padding: 12px;
                    gap: 4px;
                    flex: 1;
                }

                button {
                    all: unset;
                    cursor: pointer;
                    padding: 12px 16px;
                    border-radius: 10px;
                    transition: background .2s;
                }

                button:hover {
                    background: var(--secondary-background-color);
                }

                button.active {
                    background: var(--primary-color);
                    color: white;
                    font-weight: 600;
                }

            </style>

            <div class="title">
                OpenDoser
            </div>

            <nav>
                ${this._items.map(item => `
                    <button
                        class="${item.id === this._selected ? "active" : ""}"
                        data-page="${item.id}">
                        ${item.title}
                    </button>
                `).join("")}
            </nav>
        `;

        this.shadowRoot
            .querySelectorAll("button")
            .forEach(button => {

                button.onclick = () => {

                    if (this._callback) {
                        this._callback(
                            button.dataset.page,
                        );
                    };

                };

            });

    }

}

customElements.define(
    "od-sidebar",
    ODSidebar,
);