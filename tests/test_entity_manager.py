"""Tests for the entity manager."""

from unittest.mock import MagicMock

from custom_components.opendoser.entity_manager import EntityManager
from custom_components.opendoser.registry import RoleRegistry
from custom_components.opendoser.roles import Role


def test_assign_entity() -> None:
    """Assigning an entity should update the registry."""

    hass = MagicMock()

    registry = RoleRegistry()

    manager = EntityManager(
        hass,
        registry,
    )

    manager.assign(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    assert registry.get(Role.PH_SENSOR) == "sensor.ph"


def test_get_entity() -> None:
    """Assigned entities should be returned."""

    hass = MagicMock()

    registry = RoleRegistry()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    manager = EntityManager(
        hass,
        registry,
    )

    assert (
        manager.get_entity(
            Role.PH_SENSOR,
        )
        == "sensor.ph"
    )


def test_get_entity_unknown() -> None:
    """Unknown roles should return None."""

    hass = MagicMock()

    registry = RoleRegistry()

    manager = EntityManager(
        hass,
        registry,
    )

    assert (
        manager.get_entity(
            Role.PH_SENSOR,
        )
        is None
    )


def test_get_state() -> None:
    """The Home Assistant state should be returned."""

    hass = MagicMock()

    state = MagicMock()

    hass.states.get.return_value = state

    registry = RoleRegistry()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    manager = EntityManager(
        hass,
        registry,
    )

    assert (
        manager.get_state(
            Role.PH_SENSOR,
        )
        is state
    )

    hass.states.get.assert_called_once_with(
        "sensor.ph",
    )


def test_get_state_without_assignment() -> None:
    """Unassigned roles should return None."""

    hass = MagicMock()

    registry = RoleRegistry()

    manager = EntityManager(
        hass,
        registry,
    )

    assert (
        manager.get_state(
            Role.PH_SENSOR,
        )
        is None
    )

    hass.states.get.assert_not_called()