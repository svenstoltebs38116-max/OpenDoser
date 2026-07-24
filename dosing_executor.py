"""Executes a dosing plan."""

from __future__ import annotations

from time import monotonic

from .model.dosing_plan import DosingAction
from .model.dosing_plan import DosingPlan
from .model.execution_result import ExecutionResult
from .pump_driver import PumpDriver


class DosingExecutor:
    """Executes dosing plans."""

    def __init__(
        self,
        driver: PumpDriver,
    ) -> None:
        """Initialize the executor."""

        self._driver = driver
        self._running = False
        self._cancel_requested = False

    @property
    def running(self) -> bool:
        """Return whether execution is active."""

        return self._running

    @property
    def cancelled(self) -> bool:
        """Return whether cancellation has been requested."""

        return self._cancel_requested

    async def execute(
        self,
        plan: DosingPlan,
    ) -> ExecutionResult:
        """Execute a dosing plan."""

        if self._running:
            raise RuntimeError("Executor is already running.")

        result = ExecutionResult()

        self._running = True
        self._cancel_requested = False

        start_time = monotonic()

        try:
            for action in plan.actions:
                if self._cancel_requested:
                    result.cancelled = True
                    break

                await self.execute_action(action)
                result.actions_executed += 1

            result.completed = not result.cancelled

        except Exception as err:
            result.error = str(err)
            result.completed = False

        finally:
            result.duration_seconds = monotonic() - start_time
            self._running = False
            self._cancel_requested = False

        return result

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute one dosing action."""

        await self._driver.execute_action(action)

    def stop(self) -> None:
        """Request cancellation of the current execution."""

        self._cancel_requested = True