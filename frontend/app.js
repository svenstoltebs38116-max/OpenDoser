import OpenDoserAPI from "./api.js";

export default class OpenDoserApp {

    constructor(hass) {

        this.hass = hass;

        this.api = new OpenDoserAPI(hass);

        this.system = null;

    }

    async load() {

        this.system = await this.api.system();

        return this.system;

    }

    async create(object, data) {

        await this.api.create(
            object,
            data,
        );

        return this.load();

    }

    async update(object, data) {

        await this.api.update(
            object,
            data,
        );

        return this.load();

    }

    async delete(object, id) {

        await this.api.delete(
            object,
            id,
        );

        return this.load();

    }

}