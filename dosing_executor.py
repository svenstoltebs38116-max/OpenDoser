"""Executes a dosing plan."""

from __future__ import annotations

from .model.dosing_plan import DosingAction
from .model.dosing_plan import DosingPlan


class DosingExecutor:
    """Executes dosing plans."""

    def __init__(self) -> None:
        """Initialize the executor."""

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
    ) -> None:
        """Execute a dosing plan."""

        if self._running:
            raise RuntimeError("Executor is already running.")

        self._running = True
        self._cancel_requested = False

        try:
            for action in plan.actions:
                if self._cancel_requested:
                    break

                await self.execute_action(action)

        finally:
            self._running = False
            self._cancel_requested = False

    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute one dosing action."""

        #
        # Placeholder.
        #
        # Actual pump control will be implemented later.
        #

        return

    def stop(self) -> None:
        """Request cancellation of the current execution."""

        self._cancel_requested = True