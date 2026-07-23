export class ODCard extends HTMLElement {

    static get observedAttributes() {
        return [
            "title",
            "subtitle",
        ];
    }

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this._title = "";
        this._subtitle = "";

    }

    attributeChangedCallback(name, oldValue, newValue) {

        if (oldValue === newValue) {
            return;
        }

        if (name === "title") {
            this._title = newValue ?? "";
        }

        if (name === "subtitle") {
            this._subtitle = newValue ?? "";
        }

        this.render();

    }

    set title(value) {

        this._title = value ?? "";

        this.setAttribute("title", this._title);

    }

    get title() {
        return this._title;
    }

    set subtitle(value) {

        this._subtitle = value ?? "";

        if (this._subtitle) {
            this.setAttribute("subtitle", this._subtitle);
        } else {
            this.removeAttribute("subtitle");
        }

    }

    get subtitle() {
        return this._subtitle;
    }

    connectedCallback() {

        this._title = this.getAttribute("title") ?? "";
        this._subtitle = this.getAttribute("subtitle") ?? "";

        this.render();

    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display: block;
                }

                .card {
                    display: flex;
                    flex-direction: column;
                    background: var(--card-background-color);
                    border: 1px solid var(--divider-color);
                    border-radius: 12px;
                    overflow: hidden;
                }

                .header {
                    padding: 20px 24px;
                    border-bottom: 1px solid var(--divider-color);
                }

                .title {
                    font-size: 20px;
                    font-weight: 600;
                    color: var(--primary-text-color);
                }

                .subtitle {
                    margin-top: 4px;
                    font-size: 14px;
                    color: var(--secondary-text-color);
                }

                .content {
                    padding: 24px;
                }

            </style>

            <div class="card">

                <div class="header">

                    <div class="title">
                        ${this._title}
                    </div>

                    ${
                        this._subtitle
                            ? `
                    <div class="subtitle">
                        ${this._subtitle}
                    </div>
                    `
                            : ""
                    }

                </div>

                <div class="content">
                    <slot></slot>
                </div>

            </div>
        `;

    }

}

customElements.define(
    "od-card",
    ODCard,
);