"""Home Assistant services for OpenDoser."""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN
from .exceptions import ValidationError
from .services.system_service import SystemService

_LOGGER = logging.getLogger(__name__)


async def async_setup_services(hass: HomeAssistant) -> None:
    """Register OpenDoser services."""

    async def create_pump(call: ServiceCall) -> None:
        """Create a pump."""

        coordinator = _coordinator(
            hass,
            call,
        )

        service = SystemService(
            coordinator.system,
        )

        try:
            service.create_pump(
                id=call.data["id"],
                name=call.data["name"],
                entity_id=call.data.get(
                    "entity_id",
                    "",
                ),
            )

            await coordinator.save_system()
            await coordinator.async_request_refresh()

        except ValidationError as err:
            raise HomeAssistantError(str(err)) from err

    hass.services.async_register(
        DOMAIN,
        "create_pump",
        create_pump,
        schema=vol.Schema(
            {
                vol.Required("id"): str,
                vol.Required("name"): str,
                vol.Optional(
                    "entity_id",
                    default="",
                ): str,
            }
        ),
    )


async def async_unload_services(
    hass: HomeAssistant,
) -> None:
    """Unregister OpenDoser services."""

    hass.services.async_remove(
        DOMAIN,
        "create_pump",
    )


def _coordinator(
    hass: HomeAssistant,
    call: ServiceCall,
):
    """Return the coordinator."""

    coordinators = hass.data.get(
        DOMAIN,
        {},
    )

    if not coordinators:
        raise HomeAssistantError(
            "OpenDoser is not loaded."
        )

    #
    # Currently only one config entry is supported.
    #

    return next(
        iter(
            coordinators.values(),
        )
    )