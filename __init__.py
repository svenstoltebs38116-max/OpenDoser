"""The OpenDoser integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .coordinator import OpenDoserCoordinator


async def async_setup(
    hass: HomeAssistant,
    config: dict,
) -> bool:
    """Set up OpenDoser."""

    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Set up OpenDoser from a config entry."""

    coordinator = OpenDoserCoordinator(
        hass,
        entry,
    )

    await coordinator.async_initialize()
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(
        entry,
        [
            "binary_sensor",
            "sensor",
        ],
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
) -> bool:
    """Unload OpenDoser."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        [
            "binary_sensor",
            "sensor",
        ],
    )

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok