"""Services for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant, ServiceCall

from .const import DOMAIN
from .coordinator import OpenDoserCoordinator


async def async_register_services(
    hass: HomeAssistant,
    coordinator: OpenDoserCoordinator,
) -> None:
    """Register OpenDoser services."""

    async def execute_service(
        call: ServiceCall,
    ) -> None:
        """Execute a dosing cycle."""

        #
        # Placeholder.
        #
        # The actual execution will be implemented
        # after the executor is connected.
        #

        return

    if hass.services.has_service(
        DOMAIN,
        "execute",
    ):
        return

    hass.services.async_register(
        DOMAIN,
        "execute",
        execute_service,
    )