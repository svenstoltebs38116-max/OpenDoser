"""Tests for the role registry."""

from custom_components.opendoser.registry import RoleRegistry
from custom_components.opendoser.roles import Role


def test_registry_initially_empty() -> None:
    """A new registry should be empty."""

    registry = RoleRegistry()

    assert registry.all() == {}


def test_set_and_get_role() -> None:
    """Assigned roles should be returned."""

    registry = RoleRegistry()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    assert (
        registry.get(
            Role.PH_SENSOR,
        )
        == "sensor.ph"
    )


def test_exists() -> None:
    """exists() should reflect assignments."""

    registry = RoleRegistry()

    assert not registry.exists(
        Role.PH_SENSOR,
    )

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    assert registry.exists(
        Role.PH_SENSOR,
    )


def test_remove() -> None:
    """Removing a role should clear it."""

    registry = RoleRegistry()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    registry.remove(
        Role.PH_SENSOR,
    )

    assert (
        registry.get(
            Role.PH_SENSOR,
        )
        is None
    )

    assert not registry.exists(
        Role.PH_SENSOR,
    )


def test_all_returns_copy() -> None:
    """all() should return a copy."""

    registry = RoleRegistry()

    registry.set(
        Role.PH_SENSOR,
        "sensor.ph",
    )

    data = registry.all()

    data.clear()

    assert registry.exists(
        Role.PH_SENSOR,
    )