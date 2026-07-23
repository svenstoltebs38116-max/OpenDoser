"""OpenDoser dosing planner."""

from __future__ import annotations

from .dosing_calculator import DosingCalculator
from .model.dosing_plan import DosingPlan
from .model.feed_program import FeedProgram
from .model.feed_program_nutrient import FeedProgramNutrient
from .model.recipe import Recipe
from .model.system import System
from .model.system_state import SystemState


class DosingPlanner:
    """Creates dosing plans."""

    def __init__(self) -> None:
        """Initialize the planner."""

        self._calculator = DosingCalculator()

    def create_plan(
        self,
        system: System,
        recipe: Recipe,
        feed_program: FeedProgram,
        state: SystemState,
    ) -> DosingPlan:
        """Create a dosing plan."""

        plan = DosingPlan()

        self._plan_ph(
            plan,
            system,
            recipe,
            feed_program,
            state,
        )

        self._plan_ec(
            plan,
            system,
            recipe,
            feed_program,
            state,
        )

        return plan

    def _plan_ph(
        self,
        plan: DosingPlan,
        system: System,
        recipe: Recipe,
        feed_program: FeedProgram,
        state: SystemState,
    ) -> None:
        """Create pH correction actions."""

        if (
            state.ph is None
            or recipe.ph_in_range(state.ph)
        ):
            return

        delta = abs(
            recipe.target_ph - state.ph
        )

        nutrient_id = (
            feed_program.ph_up_nutrient_id
            if state.ph < recipe.target_ph
            else feed_program.ph_down_nutrient_id
        )

        if nutrient_id is None:
            return

        nutrient = system.get_nutrient(
            nutrient_id,
        )

        if nutrient is None:
            return

        pump = system.get_pump(
            nutrient.pump_id,
        )

        if pump is None:
            return

        volume = self._calculator.calculate_ph_volume(
            nutrient=nutrient,
            delta=delta,
            water_volume_liters=system.water_volume_liters,
        )

        if volume <= 0:
            return

        plan.add(
            pump_id=pump.id,
            volume_ml=volume,
            runtime_seconds=pump.runtime_for(
                volume,
            ),
            reason="pH correction",
        )

    def _plan_ec(
        self,
        plan: DosingPlan,
        system: System,
        recipe: Recipe,
        feed_program: FeedProgram,
        state: SystemState,
    ) -> None:
        """Create EC correction actions."""

        if (
            state.ec is None
            or recipe.ec_in_range(state.ec)
        ):
            return

        delta = recipe.target_ec - state.ec

        if delta <= 0:
            return

        nutrients = self._enabled_ec_nutrients(
            feed_program,
        )

        if not nutrients:
            return

        volumes = self._calculator.calculate_ec_volumes(
            system=system,
            nutrients=nutrients,
            delta=delta,
        )

        for nutrient_id, volume in volumes.items():

            nutrient = system.get_nutrient(
                nutrient_id,
            )

            if nutrient is None:
                continue

            pump = system.get_pump(
                nutrient.pump_id,
            )

            if pump is None:
                continue

            plan.add(
                pump_id=pump.id,
                volume_ml=volume,
                runtime_seconds=pump.runtime_for(
                    volume,
                ),
                reason="EC correction",
            )

    def _enabled_ec_nutrients(
        self,
        feed_program: FeedProgram,
    ) -> list[FeedProgramNutrient]:
        """Return enabled EC nutrients."""

        nutrients = [
            entry
            for entry in feed_program.ec_nutrients
            if entry.valid
        ]

        nutrients.sort(
            key=lambda entry: entry.priority,
        )

        return nutrients