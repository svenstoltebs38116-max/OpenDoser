"""OpenDoser dosing executor."""

from __future__ import annotations

from collections.abc import Awaitable, Callable

from .model.dosing_plan import DosingPlan

PumpRunner = Callable[[str, float], Awaitable[None]]


class DosingExecutor:
    """Executes a dosing plan."""

    def __init__(
        self,
        runner: PumpRunner,
    ) -> None:
        """Initialize the executor."""

        self._runner = runner

    async def execute(
        self,
        plan: DosingPlan,
    ) -> None:
        """Execute a dosing plan."""

        for action in plan.actions:

            await self._runner(
                action.pump_id,
                action.runtime_seconds,
            )