"""Tests for OpenDoser services."""

from __future__ import annotations

from unittest.mock import AsyncMock, Mock

import pytest

from custom_components.opendoser.services import async_register_services


class FakeServices:
    """Fake Home Assistant service registry."""

    def __init__(self) -> None:
        """Initialize."""

        self._services: dict[
            tuple[str, str],
            object,
        ] = {}

    def has_service(
        self,
        domain: str,
        service: str,
    ) -> bool:
        """Return whether the service exists."""

        return (domain, service) in self._services

    def async_register(
        self,
        domain: str,
        service: str,
        handler,
    ) -> None:
        """Register a service."""

        self._services[(domain, service)] = handler

    def get(
        self,
        domain: str,
        service: str,
    ):
        """Return a registered handler."""

        return self._services[(domain, service)]


class FakeHass:
    """Minimal Home Assistant."""

    def __init__(self) -> None:
        """Initialize."""

        self.services = FakeServices()


@pytest.mark.asyncio
async def test_register_services() -> None:
    """Services should be registered."""

    hass = FakeHass()

    coordinator = Mock()
    coordinator.async_execute_plan = AsyncMock()
    coordinator.stop_execution = Mock()

    await async_register_services(
        hass,
        coordinator,
    )

    assert hass.services.has_service(
        "opendoser",
        "execute",
    )

    assert hass.services.has_service(
        "opendoser",
        "stop",
    )


@pytest.mark.asyncio
async def test_execute_service() -> None:
    """Execute service should start execution."""

    hass = FakeHass()

    coordinator = Mock()
    coordinator.async_execute_plan = AsyncMock()
    coordinator.stop_execution = Mock()

    await async_register_services(
        hass,
        coordinator,
    )

    handler = hass.services.get(
        "opendoser",
        "execute",
    )

    await handler(None)

    coordinator.async_execute_plan.assert_awaited_once()


@pytest.mark.asyncio
async def test_stop_service() -> None:
    """Stop service should stop execution."""

    hass = FakeHass()

    coordinator = Mock()
    coordinator.async_execute_plan = AsyncMock()
    coordinator.stop_execution = Mock()

    await async_register_services(
        hass,
        coordinator,
    )

    handler = hass.services.get(
        "opendoser",
        "stop",
    )

    await handler(None)

    coordinator.stop_execution.assert_called_once()