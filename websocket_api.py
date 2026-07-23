"""WebSocket API for OpenDoser."""

from __future__ import annotations

import voluptuous as vol

from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .exceptions import ValidationError
from .services.system_service import SystemService


OBJECTS = [
    "pump",
    "tank",
    "nutrient",
    "recipe",
    "feed_program",
]


def _coordinator(
    hass: HomeAssistant,
):
    """Return the active coordinator."""

    coordinators = hass.data.get(
        DOMAIN,
        {},
    )

    if not coordinators:
        raise ValueError("OpenDoser is not loaded.")

    return next(iter(coordinators.values()))


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/system",
    }
)
@websocket_api.async_response
async def websocket_system(
    hass: HomeAssistant,
    connection,
    msg,
):
    """Return the complete system."""

    coordinator = _coordinator(hass)

    connection.send_result(
        msg["id"],
        coordinator.system.to_dict(),
    )


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/create",
        vol.Required("object"): vol.In(OBJECTS),
        vol.Required("data"): dict,
    }
)
@websocket_api.async_response
async def websocket_create(
    hass: HomeAssistant,
    connection,
    msg,
):
    """Create an object."""

    coordinator = _coordinator(hass)

    service = SystemService(
        coordinator.system,
    )

    data = msg["data"]

    try:

        match msg["object"]:

            case "pump":
                service.create_pump(**data)

            case "tank":
                service.create_tank(**data)

            case "nutrient":
                service.create_nutrient(**data)

            case "recipe":
                service.create_recipe(**data)

            case "feed_program":
                service.create_feed_program(**data)

        await coordinator.save_system()
        await coordinator.async_request_refresh()

        connection.send_result(
            msg["id"],
            {},
        )

    except ValidationError as err:

        connection.send_error(
            msg["id"],
            "validation_error",
            str(err),
        )


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/update",
        vol.Required("object"): vol.In(OBJECTS),
        vol.Required("data"): dict,
    }
)
@websocket_api.async_response
async def websocket_update(
    hass: HomeAssistant,
    connection,
    msg,
):
    """Update an object."""

    coordinator = _coordinator(hass)

    service = SystemService(
        coordinator.system,
    )

    data = msg["data"]

    try:

        match msg["object"]:

            case "pump":
                service.update_pump(**data)

            case "tank":
                service.update_tank(**data)

            case "nutrient":
                service.update_nutrient(**data)

            case "recipe":
                service.update_recipe(**data)

            case "feed_program":
                service.update_feed_program(**data)

        await coordinator.save_system()
        await coordinator.async_request_refresh()

        connection.send_result(
            msg["id"],
            {},
        )

    except ValidationError as err:

        connection.send_error(
            msg["id"],
            "validation_error",
            str(err),
        )


@websocket_api.websocket_command(
    {
        vol.Required("type"): f"{DOMAIN}/delete",
        vol.Required("object"): vol.In(OBJECTS),
        vol.Required("id"): str,
    }
)
@websocket_api.async_response
async def websocket_delete(
    hass: HomeAssistant,
    connection,
    msg,
):
    """Delete an object."""

    coordinator = _coordinator(hass)

    service = SystemService(
        coordinator.system,
    )

    try:

        match msg["object"]:

            case "pump":
                service.remove_pump(msg["id"])

            case "tank":
                service.remove_tank(msg["id"])

            case "nutrient":
                service.remove_nutrient(msg["id"])

            case "recipe":
                service.remove_recipe(msg["id"])

            case "feed_program":
                service.remove_feed_program(msg["id"])

        await coordinator.save_system()
        await coordinator.async_request_refresh()

        connection.send_result(
            msg["id"],
            {},
        )

    except ValidationError as err:

        connection.send_error(
            msg["id"],
            "validation_error",
            str(err),
        )


def async_setup_websocket_api(
    hass: HomeAssistant,
) -> None:
    """Register websocket commands."""

    websocket_api.async_register_command(
        hass,
        websocket_system,
    )

    websocket_api.async_register_command(
        hass,
        websocket_create,
    )

    websocket_api.async_register_command(
        hass,
        websocket_update,
    )

    websocket_api.async_register_command(
        hass,
        websocket_delete,
    )