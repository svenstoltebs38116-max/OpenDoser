"""Entity manager for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .registry import RoleRegistry
from .roles import Role


class EntityManager:
    """Manages role to entity assignments."""

    def __init__(
        self,
        hass: HomeAssistant,
        registry: RoleRegistry,
    ) -> None:
        """Initialize entity manager."""

        self.hass = hass
        self.registry = registry

    def assign(
        self,
        role: Role,
        entity_id: str,
    ) -> None:
        """Assign an entity to a role."""

        self.registry.set(role, entity_id)

    def get_entity(
        self,
        role: Role,
    ) -> str | None:
        """Return the assigned entity."""

        return self.registry.get(role)

    def get_state(
        self,
        role: Role,
    ):
        """Return the current Home Assistant state."""

        entity_id = self.get_entity(role)

        if entity_id is None:
            return None

        return self.hass.states.get(entity_id)