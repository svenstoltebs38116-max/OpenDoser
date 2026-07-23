const DOMAIN = "opendoser";

export default class OpenDoserAPI {

    constructor(hass) {
        this.hass = hass;
    }

    async system() {
        return this._call(
            "system",
            {}
        );
    }

    async create(object, data) {
        return this._call(
            "create",
            {
                object,
                data,
            },
        );
    }

    async update(object, data) {
        return this._call(
            "update",
            {
                object,
                data,
            },
        );
    }

    async delete(object, id) {
        return this._call(
            "delete",
            {
                object,
                id,
            },
        );
    }

    async _call(command, data = {}) {
        return this.hass.callWS({
            type: `${DOMAIN}/${command}`,
            ...data,
        });
    }

}