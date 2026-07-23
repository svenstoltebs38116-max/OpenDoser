"""Tests for the OpenDoser coordinator."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from custom_components.opendoser.coordinator import (
    OpenDoserCoordinator,
)
from custom_components.opendoser.model.dosing_plan import DosingPlan
from custom_components.opendoser.roles import Role

from .helpers import (
    create_recipe,
    create_state,
    create_system,
)


@pytest.fixture
def coordinator() -> OpenDoserCoordinator:
    """Create a coordinator."""

    hass = MagicMock()

    entry = MagicMock()

    entry.data = {}

    coordinator = OpenDoserCoordinator(
        hass,
        entry,
    )

    return coordinator


@pytest.mark.asyncio
async def test_async_initialize(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Initialization should load the system."""

    system = create_system(
        recipe=create_recipe(),
    )

    coordinator.storage.load = AsyncMock(
        return_value=system,
    )

    await coordinator.async_initialize()

    coordinator.storage.load.assert_awaited_once()

    assert coordinator.system is system


@pytest.mark.asyncio
async def test_update_requires_initialization(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Updating before initialization should fail."""

    coordinator.system = None

    with pytest.raises(RuntimeError):
        await coordinator._async_update_data()


@pytest.mark.asyncio
async def test_update_calculates_plan(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Updating should calculate a dosing plan."""

    system = create_system(
        recipe=create_recipe(),
    )

    coordinator.system = system

    coordinator.engine.calculate = MagicMock(
        return_value=DosingPlan(),
    )

    coordinator.get_role_value = MagicMock(
        side_effect=[
            6.0,
            1.6,
            20.0,
        ],
    )

    coordinator.entity_manager.get_state = MagicMock(
        return_value=None,
    )

    data = await coordinator._async_update_data()

    coordinator.engine.calculate.assert_called_once()

    assert coordinator.last_plan is not None

    assert isinstance(
        data,
        dict,
    )


@pytest.mark.asyncio
async def test_save_system(
    coordinator: OpenDoserCoordinator,
) -> None:
    """The current system should be saved."""

    system = create_system(
        recipe=create_recipe(),
    )

    coordinator.system = system

    coordinator.storage.save = AsyncMock()

    await coordinator.save_system()

    coordinator.storage.save.assert_awaited_once_with(
        system,
    )


@pytest.mark.asyncio
async def test_save_system_without_system(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Saving without a system should do nothing."""

    coordinator.system = None

    coordinator.storage.save = AsyncMock()

    await coordinator.save_system()

    coordinator.storage.save.assert_not_called()


def test_resource(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Resources should be returned."""

    resource = coordinator.resource(
        Role.PH_SENSOR,
    )

    assert resource.role == Role.PH_SENSOR


def test_get_role_state(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Role states should be delegated."""

    state = MagicMock()

    coordinator.entity_manager.get_state = MagicMock(
        return_value=state,
    )

    assert (
        coordinator.get_role_state(
            Role.PH_SENSOR,
        )
        is state
    )


def test_get_role_value(
    coordinator: OpenDoserCoordinator,
) -> None:
    """Numeric role values should be returned."""

    resource = MagicMock()

    resource.value = 6.25

    coordinator.resources._resources[
        Role.PH_SENSOR
    ] = resource

    assert (
        coordinator.get_role_value(
            Role.PH_SENSOR,
        )
        == 6.25
    )