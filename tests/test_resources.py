"""Tests for OpenDoser resources."""

from unittest.mock import MagicMock

from custom_components.opendoser.entity_manager import EntityManager
from custom_components.opendoser.registry import RoleRegistry
from custom_components.opendoser.resources import (
    Resource,
    ResourceManager,
    SensorResource,
    SwitchResource,
)
from custom_components.opendoser.roles import Role


def create_manager() -> tuple[MagicMock, RoleRegistry, EntityManager]:
    """Create a test entity manager."""

    hass = MagicMock()

    registry = RoleRegistry()

    manager = EntityManager(
        hass,
        registry,
    )

    return hass, registry, manager


def test_resource_entity_id() -> None:
    """The assigned entity id should be returned."""

    hass, registry, manager = create_manager()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    resource = Resource(
        hass,
        manager,
        Role.PH_SENSOR,
    )

    assert resource.entity_id == "sensor.ph"


def test_resource_available() -> None:
    """Resources with a state should be available."""

    hass, registry, manager = create_manager()

    state = MagicMock()

    hass.states.get.return_value = state

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    resource = Resource(
        hass,
        manager,
        Role.PH_SENSOR,
    )

    assert resource.available


def test_resource_unavailable() -> None:
    """Resources without a state should not be available."""

    hass, registry, manager = create_manager()

    hass.states.get.return_value = None

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    resource = Resource(
        hass,
        manager,
        Role.PH_SENSOR,
    )

    assert not resource.available


def test_sensor_resource_returns_numeric_value() -> None:
    """Numeric sensor values should be converted."""

    hass, registry, manager = create_manager()

    state = MagicMock()

    state.state = "6.25"

    hass.states.get.return_value = state

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    resource = SensorResource(
        hass,
        manager,
        Role.PH_SENSOR,
    )

    assert resource.value == 6.25


def test_sensor_resource_invalid_value() -> None:
    """Invalid sensor values should return None."""

    hass, registry, manager = create_manager()

    state = MagicMock()

    state.state = "unknown"

    hass.states.get.return_value = state

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    resource = SensorResource(
        hass,
        manager,
        Role.PH_SENSOR,
    )

    assert resource.value is None


def test_switch_resource_on() -> None:
    """Switch resources should detect the on state."""

    hass, registry, manager = create_manager()

    state = MagicMock()

    state.state = "on"

    hass.states.get.return_value = state

    registry.set(
        Role.PUMP_A,
        "switch.pump_a",
    )

    resource = SwitchResource(
        hass,
        manager,
        Role.PUMP_A,
    )

    assert resource.is_on


def test_switch_resource_off() -> None:
    """Switch resources should detect the off state."""

    hass, registry, manager = create_manager()

    state = MagicMock()

    state.state = "off"

    hass.states.get.return_value = state

    registry.set(
        Role.PUMP_A,
        "switch.pump_a",
    )

    resource = SwitchResource(
        hass,
        manager,
        Role.PUMP_A,
    )

    assert not resource.is_on


def test_resource_manager_returns_resources() -> None:
    """The resource manager should create resources."""

    hass, _, manager = create_manager()

    resources = ResourceManager(
        hass,
        manager,
    )

    resource = resources[
        Role.PH_SENSOR
    ]

    assert isinstance(
        resource,
        SensorResource,
    )


def test_resource_manager_values() -> None:
    """values() should return all resources."""

    hass, _, manager = create_manager()

    resources = ResourceManager(
        hass,
        manager,
    )

    values = list(
        resources.values()
    )

    assert values

    assert all(
        isinstance(
            resource,
            Resource,
        )
        for resource in values
    )