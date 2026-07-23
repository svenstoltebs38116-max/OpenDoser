"""Tests for the DosingExecutor."""

from __future__ import annotations

import asyncio

import pytest

from custom_components.opendoser.dosing_executor import DosingExecutor
from custom_components.opendoser.model.dosing_plan import DosingAction
from custom_components.opendoser.model.dosing_plan import DosingPlan


class RecordingExecutor(DosingExecutor):
    """Executor that records executed actions."""

    def __init__(self) -> None:
        """Initialize the executor."""
        super().__init__()
        self.executed_actions: list[DosingAction] = []

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Record executed actions."""
        self.executed_actions.append(action)


class RunningStateExecutor(DosingExecutor):
    """Executor used to verify the running state."""

    def __init__(self) -> None:
        """Initialize the executor."""
        super().__init__()
        self.running_during_execution = False

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Capture the running state."""
        self.running_during_execution = self.running
        await asyncio.sleep(0)


class FailingExecutor(DosingExecutor):
    """Executor that always fails."""

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Raise an exception."""
        raise RuntimeError("Execution failed")


class CancelExecutor(DosingExecutor):
    """Executor that requests cancellation."""

    def __init__(self) -> None:
        """Initialize the executor."""
        super().__init__()
        self.executed_actions: list[DosingAction] = []

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute one action and cancel afterwards."""
        self.executed_actions.append(action)
        self.stop()


def create_plan(count: int) -> DosingPlan:
    """Create a dosing plan with a given number of actions."""
    plan = DosingPlan()

    for index in range(count):
        plan.add(
            pump_id=f"pump_{index}",
            volume_ml=10.0,
            runtime_seconds=5.0,
            reason=f"Action {index}",
        )

    return plan


def test_running_initially_false() -> None:
    """Executor should not be running after creation."""
    executor = DosingExecutor()

    assert executor.running is False
    assert executor.cancelled is False


@pytest.mark.asyncio
async def test_execute_empty_plan() -> None:
    """Executing an empty plan should succeed."""
    executor = RecordingExecutor()
    plan = DosingPlan()

    await executor.execute(plan)

    assert executor.running is False
    assert executor.executed_actions == []


@pytest.mark.asyncio
async def test_execute_actions_in_order() -> None:
    """Actions should be executed in order."""
    executor = RecordingExecutor()
    plan = create_plan(3)

    await executor.execute(plan)

    assert executor.executed_actions == plan.actions


@pytest.mark.asyncio
async def test_running_true_during_execution() -> None:
    """Running should be true while an action is executed."""
    executor = RunningStateExecutor()
    plan = create_plan(1)

    await executor.execute(plan)

    assert executor.running_during_execution is True
    assert executor.running is False


@pytest.mark.asyncio
async def test_running_reset_after_exception() -> None:
    """Running should always be reset after an exception."""
    executor = FailingExecutor()
    plan = create_plan(1)

    with pytest.raises(RuntimeError):
        await executor.execute(plan)

    assert executor.running is False
    assert executor.cancelled is False


@pytest.mark.asyncio
async def test_execute_while_running_raises() -> None:
    """Starting execution while already running should fail."""
    executor = DosingExecutor()

    executor._running = True

    with pytest.raises(RuntimeError):
        await executor.execute(DosingPlan())

    executor._running = False


@pytest.mark.asyncio
async def test_stop_cancels_remaining_actions() -> None:
    """Execution should stop after cancellation."""
    executor = CancelExecutor()
    plan = create_plan(5)

    await executor.execute(plan)

    assert len(executor.executed_actions) == 1
    assert executor.running is False
    assert executor.cancelled is False


def test_stop() -> None:
    """Stop should request cancellation."""
    executor = DosingExecutor()

    executor.stop()

    assert executor.cancelled is True