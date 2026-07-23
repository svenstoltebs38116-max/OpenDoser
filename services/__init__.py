"""Business services for OpenDoser."""

from __future__ import annotations

import logging

from homeassistant.core import HomeAssistant, ServiceCall

from ..const import DOMAIN
from ..coordinator import OpenDoserCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_register_services(
    hass: HomeAssistant,
    coordinator: OpenDoserCoordinator,
) -> None:
    """Register OpenDoser services."""

    async def execute_service(
        call: ServiceCall,
    ) -> None:
        """Execute the current dosing plan."""

        plan = coordinator.last_plan

        if plan is None:
            _LOGGER.warning(
                "Execute requested but no dosing plan is available."
            )
        else:
            _LOGGER.info(
                "Executing dosing plan: %d action(s), %d warning(s)",
                len(plan.actions),
                len(plan.warnings),
            )

            for index, action in enumerate(
                plan.actions,
                start=1,
            ):
                _LOGGER.info(
                    "Action %d: role=%s volume=%.2f ml runtime=%.2f s reason=%s",
                    index,
                    action.role.value,
                    action.volume_ml,
                    action.runtime_seconds,
                    action.reason,
                )

            for warning in plan.warnings:
                _LOGGER.warning(
                    "Plan warning: %s",
                    warning,
                )

        result = await coordinator.async_execute_plan()

        _LOGGER.info(
            "Execution finished: completed=%s cancelled=%s executed=%d error=%s",
            result.completed,
            result.cancelled,
            result.actions_executed,
            result.error,
        )

    async def stop_service(
        call: ServiceCall,
    ) -> None:
        """Stop the current dosing execution."""

        _LOGGER.info(
            "Stopping dosing execution."
        )

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