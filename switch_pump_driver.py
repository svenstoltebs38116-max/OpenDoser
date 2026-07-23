"""Switch-based pump driver for OpenDoser."""

from __future__ import annotations

import asyncio

from homeassistant.const import SERVICE_TURN_OFF, SERVICE_TURN_ON
from homeassistant.core import HomeAssistant

from .entity_manager import EntityManager
from .model.dosing_plan import DosingAction
from .pump_driver import PumpDriver


class SwitchPumpDriver(PumpDriver):
    """Pump driver using Home Assistant switch entities."""

    def __init__(
        self,
        hass: HomeAssistant,
        entity_manager: EntityManager,
    ) -> None:
        """Initialize the switch pump driver."""

        self._hass = hass
        self._entity_manager = entity_manager

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute a dosing action."""

        state = self._entity_manager.get_state(
            action.role,
        )

        if state is None:
            raise RuntimeError(
                f"No entity configured for role {action.role.value}."
            )

        domain = state.entity_id.split(".", 1)[0]

        await self._hass.services.async_call(
            domain,
            SERVICE_TURN_ON,
            {
                "entity_id": state.entity_id,
            },
            blocking=True,
        )

        try:
            await asyncio.sleep(
                action.runtime_seconds,
            )
        finally:
            await self._hass.services.async_call(
                domain,
                SERVICE_TURN_OFF,
                {
                    "entity_id": state.entity_id,
                },
                blocking=True,
            )