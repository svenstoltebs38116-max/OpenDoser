"""Pump registry for OpenDoser."""

from __future__ import annotations


class PumpRegistry:
    """Maps logical pump IDs to Home Assistant entities."""

    def __init__(self) -> None:
        """Initialize the registry."""

        self._entities: dict[str, str] = {}

    def register(
        self,
        pump_id: str,
        entity_id: str,
    ) -> None:
        """Register a pump."""

        self._entities[pump_id] = entity_id

    def unregister(
        self,
        pump_id: str,
    ) -> None:
        """Remove a pump registration."""

        self._entities.pop(pump_id, None)

    def get_entity_id(
        self,
        pump_id: str,
    ) -> str:
        """Return the Home Assistant entity ID for a pump."""

        try:
            return self._entities[pump_id]
        except KeyError as err:
            raise KeyError(
                f"Pump '{pump_id}' is not registered."
            ) from err

    def is_registered(
        self,
        pump_id: str,
    ) -> bool:
        """Return whether a pump is registered."""

        return pump_id in self._entities

    def clear(self) -> None:
        """Remove all registrations."""

        self._entities.clear()