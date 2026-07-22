"""Config flow for OpenDoser."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant, callback

from .const import DOMAIN
from .roles import ROLE_DEFINITIONS

_LOGGER = logging.getLogger(__name__)


def _entity_choices(hass: HomeAssistant, domain: str) -> dict[str, str]:
    """Return all entities for a domain."""

    entities: dict[str, str] = {}

    for state in sorted(
        hass.states.async_all(domain),
        key=lambda s: s.name.lower(),
    ):
        entities[state.entity_id] = state.name

    return entities


class OpenDoserConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle OpenDoser config flow."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Initial setup."""

        if user_input is not None:
            return self.async_create_entry(
                title=user_input["name"],
                data=user_input,
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "name",
                        default="OpenDoser",
                    ): str,
                }
            ),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return options flow."""

        return OpenDoserOptionsFlow(config_entry)


class OpenDoserOptionsFlow(config_entries.OptionsFlow):
    """OpenDoser options."""

    def __init__(self, config_entry):
        """Initialize."""

        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Configure role assignments."""

        if user_input is not None:
            _LOGGER.info("Role assignments: %s", user_input)

            return self.async_create_entry(
                title="",
                data=user_input,
            )

        options = self._config_entry.options

        schema: dict = {}

        for role, definition in ROLE_DEFINITIONS.items():

            entities = _entity_choices(
                self.hass,
                definition.domain,
            )

            if definition.optional:
                entities = {
                    "": "--- not used ---",
                    **entities,
                }

                schema[
                    vol.Optional(
                        role.value,
                        default=options.get(role.value, ""),
                    )
                ] = vol.In(entities)

            else:
                default = options.get(role.value)

                if default is None:
                    default = next(iter(entities), "")

                schema[
                    vol.Required(
                        role.value,
                        default=default,
                    )
                ] = vol.In(entities)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(schema),
        )