"""The OpenDoser integration."""

from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import OpenDoserCoordinator
from .panel import async_setup_panel
from .services import async_register_services
from .websocket_api import async_setup_websocket_api

PLATFORMS = ["sensor"]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up OpenDoser."""

    hass.data.setdefault(DOMAIN, {})

    #
    # Register static frontend files
    #

    frontend_path = (
        Path(__file__).parent / "frontend"
    )

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"/{DOMAIN}/frontend",
                path=str(frontend_path),
                cache_headers=False,
            ),
        ]
    )

    #
    # Register websocket API
    #

    async_setup_websocket_api(
        hass,
    )

    #
    # Register sidebar panel
    #

    await async_setup_panel(
        hass,
    )

    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up OpenDoser."""

    coordinator = OpenDoserCoordinator(
        hass,
        entry,
    )

    #
    # Load persistent configuration
    #

    await coordinator.async_initialize()

    #
    # Register services
    #

    await async_register_services(
        hass,
        coordinator,
    )

    #
    # Start coordinator
    #

    await coordinator.async_config_entry_first_refresh()

    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload OpenDoser."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(
            entry.entry_id,
        )

    return unload_ok