"""Business services for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall

from ..const import DOMAIN
from ..coordinator import OpenDoserCoordinator


async def async_register_services(
    hass: HomeAssistant,
    coordinator: OpenDoserCoordinator,
) -> None:
    """Register OpenDoser services."""

    async def execute_service(
        call: ServiceCall,
    ) -> None:
        """Execute the current dosing plan."""

        await coordinator.async_execute_plan()

    async def stop_service(
        call: ServiceCall,
    ) -> None:
        """Stop the current dosing execution."""

        coordinator.stop_execution()

    if not hass.services.has_service(
        DOMAIN,
        "execute",
    ):
        hass.services.async_register(
            DOMAIN,
            "execute",
            execute_service,
        )

    if not hass.services.has_service(
        DOMAIN,
        "stop",
    ):
        hass.services.async_register(
            DOMAIN,
            "stop",
            stop_service,
        )