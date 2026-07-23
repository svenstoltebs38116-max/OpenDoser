"""Switch-based pump driver for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant

from .model.dosing_plan import DosingAction
from .pump_driver import PumpDriver


class SwitchPumpDriver(PumpDriver):
    """Pump driver using Home Assistant switch entities."""

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize the switch pump driver."""

        self._hass = hass

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute a dosing action."""

        #
        # This is intentionally only a skeleton.
        #
        # A future step will resolve action.pump_id to the configured
        # Home Assistant entity_id and determine how long the pump
        # should remain enabled.
        #
        raise NotImplementedError(
            "SwitchPumpDriver is not implemented yet."
        )