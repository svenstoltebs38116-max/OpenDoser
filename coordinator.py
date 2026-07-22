"""Coordinator for OpenDoser."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .engine import OpenDoserEngine
from .entity_manager import EntityManager
from .model.nutrient import Nutrient
from .model.recipe import Recipe
from .model.system import System
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
        # Domain model
        #

        self.system = System(
            recipe=Recipe(
                id="default",
                name="Default Recipe",
            )
        )

        #
        # Temporary nutrients
        #

        self.system.add_nutrient(
            Nutrient(
                id="ph_down",
                name="pH Down",
                pump_id="pump_ph_down",
                tank_id="tank_ph_down",
                strength=0.05,
            )
        )

        self.system.add_nutrient(
            Nutrient(
                id="ec",
                name="EC",
                pump_id="pump_ec",
                tank_id="tank_ec",
                strength=0.10,
            )
        )

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