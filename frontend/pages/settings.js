import BasePage from "./base_page.js";

export default class SettingsPage extends BasePage {

    get pageId() {
        return "settings";
    }

    get pageTitle() {
        return "Settings";
    }

    get toolbarActions() {
        return [];
    }

    async renderPage() {

        return `
            <od-card title="Settings">

                <p>
                    Configuration options for OpenDoser will be available here.
                </p>

            </od-card>

            <style>

                p {

                    margin: 0;

                    line-height: 1.6;

                }

            </style>
        `;

    }

}

customElements.define(
    "od-page-settings",
    SettingsPage,
);