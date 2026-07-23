"""Coordinator for OpenDoser."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .engine import OpenDoserEngine
from .entity_manager import EntityManager
from .model.execution_result import ExecutionResult
from .model.system import System
from .model.system_state import SystemState
from .registry import RoleRegistry
from .resources import ResourceManager
from .roles import ROLE_DEFINITIONS, Role
from .storage import SystemStorage
from .switch_pump_driver import SwitchPumpDriver

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
        # Storage
        #

        self.storage = SystemStorage(hass)

        self.system: System | None = None

        #
        # Runtime
        #

        self.driver = SwitchPumpDriver(
            hass,
            self.entity_manager,
        )

        self.engine = OpenDoserEngine(
            self.driver,
        )

        self.system_state = SystemState()

        self.last_plan = None

    async def async_initialize(self) -> None:
        """Load persistent configuration."""

        self.system = await self.storage.load()

    async def _async_update_data(self):
        """Fetch current data."""

        if self.system is None:
            raise RuntimeError("Coordinator not initialized")

        ph = self.get_role_value(Role.PH_SENSOR)
        ec = self.get_role_value(Role.EC_SENSOR)
        temperature = self.get_role_value(Role.TEMPERATURE_SENSOR)

        _LOGGER.warning(
            "OpenDoser sensor values: ph=%r ec=%r temperature=%r",
            ph,
            ec,
            temperature,
        )

        self.system_state = SystemState(
            ph=ph,
            ec=ec,
            temperature=temperature,
            tds=None,
            salinity=None,
        )

        _LOGGER.warning(
            "SystemState.available=%s",
            self.system_state.available,
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

    async def async_execute_plan(
        self,
    ) -> ExecutionResult:
        """Execute the current dosing plan."""

        if self.last_plan is None:
            raise RuntimeError(
                "No dosing plan available."
            )

        return await self.engine.execute(
            self.last_plan,
        )

    def stop_execution(
        self,
    ) -> None:
        """Stop the current execution."""

        self.engine.stop()

    async def save_system(self) -> None:
        """Persist the current system."""

        if self.system is not None:
            await self.storage.save(self.system)

    def resource(
        self,
        role: Role,
    ):
        """Return resource."""

        return self.resources[role]

    def get_role_state(
        self,
        role: Role,
    ):
        """Return Home Assistant state."""

        return self.entity_manager.get_state(role)

    def get_role_value(
        self,
        role: Role,
    ):
        """Return numeric value if available."""

        resource = self.resources[role]

        return getattr(resource, "value", None)