"""Tests for the SwitchPumpDriver."""

from __future__ import annotations

import asyncio

import pytest

from custom_components.opendoser.model.dosing_plan import DosingAction
from custom_components.opendoser.roles import Role
from custom_components.opendoser.switch_pump_driver import SwitchPumpDriver


class FakeState:
    """Minimal Home Assistant state."""

    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
        self.state = "off"
        self.attributes = {}


class FakeEntityManager:
    """Minimal EntityManager."""

    def get_state(
        self,
        role: Role,
    ):
        if role == Role.PH_UP_PUMP:
            return FakeState("switch.ph_up")

        return None


class FakeServices:
    """Record service calls."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    async def async_call(
        self,
        domain: str,
        service: str,
        service_data: dict,
        blocking: bool = False,
    ) -> None:
        self.calls.append(
            (
                domain,
                service,
                service_data,
            )
        )


class FakeHass:
    """Minimal HomeAssistant."""

    def __init__(self) -> None:
        self.services = FakeServices()


@pytest.mark.asyncio
async def test_execute_action_turns_switch_on_and_off(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A dosing action should switch the entity on and off."""

    async def fake_sleep(
        seconds: float,
    ) -> None:
        return None

    monkeypatch.setattr(
        asyncio,
        "sleep",
        fake_sleep,
    )

    hass = FakeHass()

    driver = SwitchPumpDriver(
        hass,
        FakeEntityManager(),
    )

    action = DosingAction(
        role=Role.PH_UP_PUMP,
        volume_ml=10.0,
        runtime_seconds=5.0,
        reason="Unit test",
    )

    await driver.execute_action(
        action,
    )

    assert hass.services.calls == [
        (
            "switch",
            "turn_on",
            {
                "entity_id": "switch.ph_up",
            },
        ),
        (
            "switch",
            "turn_off",
            {
                "entity_id": "switch.ph_up",
            },
        ),
    ]


@pytest.mark.asyncio
async def test_missing_entity_raises() -> None:
    """Missing entity should raise."""

    hass = FakeHass()

    driver = SwitchPumpDriver(
        hass,
        FakeEntityManager(),
    )

    action = DosingAction(
        role=Role.PH_DOWN_PUMP,
        volume_ml=10.0,
        runtime_seconds=5.0,
        reason="Unit test",
    )

    with pytest.raises(RuntimeError):
        await driver.execute_action(
            action,
        )