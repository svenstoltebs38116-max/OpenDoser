"""Sensor platform for OpenDoser."""

from __future__ import annotations

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from .const import DOMAIN
from .coordinator import OpenDoserCoordinator
from .roles import ROLE_DEFINITIONS


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up OpenDoser sensor."""

    coordinator: OpenDoserCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        [
            OpenDoserStatusSensor(
                coordinator,
            )
        ]
    )


class OpenDoserStatusSensor(SensorEntity):
    """Diagnostic sensor for OpenDoser."""

    _attr_has_entity_name = True
    _attr_name = "Status"
    _attr_unique_id = "opendoser_status"
    _attr_icon = "mdi:test-tube"

    def __init__(
        self,
        coordinator: OpenDoserCoordinator,
    ) -> None:
        """Initialize."""

        self.coordinator = coordinator

    @property
    def native_value(self):
        """Return current status."""

        if not self.coordinator.system_state.available:
            return "waiting_for_sensors"

        if self.coordinator.last_plan is None:
            return "idle"

        if self.coordinator.last_plan.warnings:
            return "warning"

        if self.coordinator.last_plan.actions:
            return "ready"

        return "idle"

    @property
    def extra_state_attributes(self):
        """Return diagnostic information."""

        assigned = 0
        missing = 0

        attributes = {}

        for role in ROLE_DEFINITIONS:

            value = self.coordinator.data.get(role.value)

            if value is None:
                missing += 1
                attributes[role.value] = None
                continue

            assigned += 1

            attributes[role.value] = {
                "entity_id": value["entity_id"],
                "state": value["state"],
            }

        attributes["configured_roles"] = len(ROLE_DEFINITIONS)
        attributes["assigned_roles"] = assigned
        attributes["missing_roles"] = missing

        if self.coordinator.last_plan is not None:
            attributes["warnings"] = list(
                self.coordinator.last_plan.warnings
            )
            attributes["planned_actions"] = len(
                self.coordinator.last_plan.actions
            )

        return attributes

    async def async_update(self):
        """Update."""

        await self.coordinator.async_request_refresh()