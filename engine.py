"""OpenDoser business logic."""

from __future__ import annotations

from .dosing_planner import DosingPlanner
from .model.dosing_plan import DosingPlan
from .model.system import System
from .model.system_state import SystemState


class OpenDoserEngine:
    """Business logic layer for OpenDoser."""

    def __init__(self) -> None:
        """Initialize the engine."""

        self._planner = DosingPlanner()

    def calculate(
        self,
        system: System,
        state: SystemState,
    ) -> DosingPlan:
        """Calculate a dosing plan."""

        plan = DosingPlan()

        #
        # Recipe enabled?
        #

        if not system.recipe.enabled:
            plan.add_warning("Recipe is disabled.")
            return plan

        #
        # Required sensors available?
        #

        if not state.available:
            plan.add_warning("Required sensors unavailable.")
            return plan

        #
        # Feed program
        #

        feed_program = None

        if system.recipe.feed_program_id is not None:
            feed_program = system.get_feed_program(
                system.recipe.feed_program_id,
            )

        if feed_program is None:
            plan.add_warning("No feed program selected.")
            return plan

        #
        # Delegate planning
        #

        return self._planner.create_plan(
            system=system,
            recipe=system.recipe,
            feed_program=feed_program,
            state=state,
        )