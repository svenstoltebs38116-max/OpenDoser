"""Entity manager for OpenDoser."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant

from .registry import RoleRegistry
from .roles import Role

_LOGGER = logging.getLogger(__name__)


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
            _LOGGER.warning(
                "Role %s has no assigned entity",
                role.value,
            )
            return None

        state = self.hass.states.get(entity_id)

        _LOGGER.warning(
            "Role=%s Entity=%s State=%s",
            role.value,
            entity_id,
            state,
        )

        return state