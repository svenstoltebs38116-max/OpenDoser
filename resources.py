"""Resource layer for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, State

from .entity_manager import EntityManager
from .roles import ROLE_DEFINITIONS, Role


class Resource:
    """Base resource."""

    def __init__(
        self,
        hass: HomeAssistant,
        manager: EntityManager,
        role: Role,
    ) -> None:
        self._hass = hass
        self._manager = manager
        self.role = role
        self.definition = ROLE_DEFINITIONS[role]

    @property
    def entity_id(self) -> str | None:
        """Assigned entity."""
        return self._manager.registry.get(self.role)

    @property
    def state(self) -> State | None:
        """Current Home Assistant state."""
        return self._manager.get_state(self.role)

    @property
    def available(self) -> bool:
        """Return availability."""
        return self.state is not None


class SensorResource(Resource):
    """Sensor resource."""

    @property
    def value(self) -> float | None:
        """Return numeric value."""
        state = self.state

        if state is None:
            return None

        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None


class SwitchResource(Resource):
    """Switch resource."""

    @property
    def is_on(self) -> bool:
        """Return switch state."""
        state = self.state

        return state is not None and state.state == "on"


class ResourceManager:
    """Creates and stores resources."""

    def __init__(
        self,
        hass: HomeAssistant,
        manager: EntityManager,
    ) -> None:
        self._resources: dict[Role, Resource] = {}

        for role, definition in ROLE_DEFINITIONS.items():

            if definition.domain == "sensor":
                resource = SensorResource(hass, manager, role)

            elif definition.domain == "switch":
                resource = SwitchResource(hass, manager, role)

            else:
                resource = Resource(hass, manager, role)

            self._resources[role] = resource

    def __getitem__(self, role: Role) -> Resource:
        """Return resource."""
        return self._resources[role]

    def values(self):
        """Return all resources."""
        return self._resources.values()