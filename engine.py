"""OpenDoser business logic."""

from __future__ import annotations

from .dosing_executor import DosingExecutor
from .dosing_planner import DosingPlanner
from .model.dosing_plan import DosingPlan
from .model.execution_result import ExecutionResult
from .model.feed_program import FeedProgram
from .model.system import System
from .model.system_state import SystemState
from .pump_driver import PumpDriver


class OpenDoserEngine:
    """Business logic layer for OpenDoser."""

    def __init__(
        self,
        driver: PumpDriver,
    ) -> None:
        """Initialize the engine."""

        self._planner = DosingPlanner()
        self._executor = DosingExecutor(driver)

    def validate(
        self,
        system: System,
        state: SystemState,
    ) -> list[str]:
        """Validate whether a dosing plan can be created."""

        warnings: list[str] = []

        if not system.recipe.enabled:
            warnings.append("Recipe is disabled.")

        missing_sensors: list[str] = []

        if state.ph is None:
            missing_sensors.append("pH Sensor")

        if state.ec is None:
            missing_sensors.append("EC Sensor")

        if state.temperature is None:
            missing_sensors.append("Temperature Sensor")

        if missing_sensors:
            warnings.append(
                "Missing sensor values: "
                + ", ".join(missing_sensors)
            )

        if system.recipe.feed_program_id is None:
            warnings.append("No feed program selected.")

        return warnings

    def get_feed_program(
        self,
        system: System,
    ) -> FeedProgram | None:
        """Return the configured feed program."""

        if system.recipe.feed_program_id is None:
            return None

        return system.get_feed_program(
            system.recipe.feed_program_id,
        )

    def calculate(
        self,
        system: System,
        state: SystemState,
    ) -> DosingPlan:
        """Calculate a dosing plan."""

        plan = DosingPlan()

        for warning in self.validate(system, state):
            plan.add_warning(warning)

        if plan.warnings:
            return plan

        feed_program = self.get_feed_program(system)

        if feed_program is None:
            plan.add_warning("Feed program not found.")
            return plan

        return self._planner.create_plan(
            system=system,
            recipe=system.recipe,
            feed_program=feed_program,
            state=state,
        )

    async def execute(
        self,
        plan: DosingPlan,
    ) -> ExecutionResult:
        """Execute a dosing plan."""

        return await self._executor.execute(plan)

    def stop(self) -> None:
        """Stop the current execution."""

        self._executor.stop()