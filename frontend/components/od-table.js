export class ODTable extends HTMLElement {

    constructor() {

        super();

        this.attachShadow({
            mode: "open",
        });

        this._columns = [];
        this._rows = [];

        this.onEdit = null;
        this.onDelete = null;

    }

    set columns(value) {

        this._columns = value ?? [];

        this.render();

    }

    set rows(value) {

        this._rows = value ?? [];

        this.render();

    }

    connectedCallback() {

        this.render();

    }

    render() {

        this.shadowRoot.innerHTML = `
            <style>

                :host {
                    display:block;
                }

                table {
                    width:100%;
                    border-collapse:collapse;
                    background:var(--card-background-color);
                    border-radius:12px;
                    overflow:hidden;
                    border:1px solid var(--divider-color);
                }

                thead {
                    background:var(--secondary-background-color);
                }

                th {
                    text-align:left;
                    padding:14px 16px;
                    font-weight:600;
                    border-bottom:1px solid var(--divider-color);
                }

                td {
                    padding:14px 16px;
                    border-bottom:1px solid var(--divider-color);
                }

                tr:last-child td {
                    border-bottom:none;
                }

                .actions {
                    white-space:nowrap;
                    width:1%;
                }

                button {

                    margin-right:8px;

                    padding:6px 12px;

                    cursor:pointer;

                }

                .empty {

                    padding:30px;

                    text-align:center;

                    color:var(--secondary-text-color);

                }

            </style>

            ${
                this._rows.length === 0
                    ? `
                <div class="empty">
                    Keine Einträge vorhanden.
                </div>
            `
                    : `
                <table>

                    <thead>

                        <tr>

                            ${this._columns.map(c => `<th>${c.label}</th>`).join("")}

                            <th class="actions"></th>

                        </tr>

                    </thead>

                    <tbody>

                        ${this._rows.map((row, index) => `
                            <tr>

                                ${this._columns.map(col => `
                                    <td>${row[col.key] ?? ""}</td>
                                `).join("")}

                                <td class="actions">

                                    <button class="edit" data-index="${index}">
                                        Bearbeiten
                                    </button>

                                    <button class="delete" data-index="${index}">
                                        Löschen
                                    </button>

                                </td>

                            </tr>
                        `).join("")}

                    </tbody>

                </table>
            `
            }
        `;

        this.shadowRoot
            .querySelectorAll(".edit")
            .forEach(button => {

                button.onclick = () => {

                    if (this.onEdit) {

                        this.onEdit(
                            this._rows[
                                Number(button.dataset.index)
                            ]
                        );

                    }

                };

            });

        this.shadowRoot
            .querySelectorAll(".delete")
            .forEach(button => {

                button.onclick = () => {

                    if (this.onDelete) {

                        this.onDelete(
                            this._rows[
                                Number(button.dataset.index)
                            ]
                        );

                    }

                };

            });

    }

}

customElements.define(
    "od-table",
    ODTable,
);