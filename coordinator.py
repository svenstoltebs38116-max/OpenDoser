"""Coordinator for OpenDoser."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .configuration import Configuration
from .engine import OpenDoserEngine
from .entity_manager import EntityManager
from .model.system_state import SystemState
from .registry import RoleRegistry
from .resources import ResourceManager
from .roles import ROLE_DEFINITIONS, Role

_LOGGER = logging.getLogger(__name__)


class OpenDoserCoordinator(DataUpdateCoordinator):
    """OpenDoser coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
    ) -> None:
        """Initialize coordinator."""

        super().__init__(
            hass=hass,
            logger=_LOGGER,
            name="OpenDoser",
            update_interval=timedelta(seconds=5),
        )

        #
        # Registry
        #

        self.registry = RoleRegistry()

        for role in ROLE_DEFINITIONS:
            entity_id = entry.data.get(role.value)

            if entity_id:
                self.registry.set(role, entity_id)

        #
        # Home Assistant adapters
        #

        self.entity_manager = EntityManager(
            hass,
            self.registry,
        )

        self.resources = ResourceManager(
            hass,
            self.entity_manager,
        )

        #
        # Domain
        #

        self.system = Configuration.create_default_system()

        #
        # Runtime
        #

        self.engine = OpenDoserEngine()

        self.system_state = SystemState()

        self.last_plan = None

    async def _async_update_data(self):
        """Fetch current data."""

        self.system_state = SystemState(
            ph=self.get_role_value(Role.PH_SENSOR),
            ec=self.get_role_value(Role.EC_SENSOR),
            temperature=self.get_role_value(Role.TEMPERATURE_SENSOR),
            tds=None,
            salinity=None,
        )

        self.last_plan = self.engine.calculate(
            self.system,
            self.system_state,
        )

        data = {}

        for role in ROLE_DEFINITIONS:
            state = self.entity_manager.get_state(role)

            if state is None:
                data[role.value] = None
                continue

            data[role.value] = {
                "entity_id": state.entity_id,
                "state": state.state,
                "attributes": dict(state.attributes),
            }

        return data

    def resource(self, role: Role):
        """Return resource."""

        return self.resources[role]

    def get_role_state(self, role: Role):
        """Return Home Assistant state."""

        return self.entity_manager.get_state(role)

    def get_role_value(self, role: Role):
        """Return numeric value if available."""

        resource = self.resources[role]

        return getattr(resource, "value", None)