"""Binary sensor platform for OpenDoser."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import OpenDoserCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up OpenDoser binary sensors."""

    coordinator: OpenDoserCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            OpenDoserReadyBinarySensor(coordinator),
        ]
    )


class OpenDoserReadyBinarySensor(
    CoordinatorEntity[OpenDoserCoordinator],
    BinarySensorEntity,
):
    """Indicates whether OpenDoser has all required sensor values."""

    _attr_has_entity_name = True
    _attr_name = "Ready"
    _attr_unique_id = "opendoser_ready"
    _attr_device_class = "connectivity"

    def __init__(
        self,
        coordinator: OpenDoserCoordinator,
    ) -> None:
        """Initialize."""

        super().__init__(coordinator)

    @property
    def is_on(self) -> bool:
        """Return readiness state."""

        return self.coordinator.system_state.available

    @property
    def extra_state_attributes(self):
        """Return diagnostic information."""

        return {
            "available": self.coordinator.system_state.available,
        }