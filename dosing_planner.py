"""OpenDoser dosing planner."""

from __future__ import annotations

from .model.dosing_plan import DosingPlan
from .model.feed_program import FeedProgram
from .model.recipe import Recipe
from .model.system import System
from .model.system_state import SystemState


class DosingPlanner:
    """Creates dosing plans."""

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

        self._add_action(
            plan=plan,
            system=system,
            nutrient_id=nutrient_id,
            delta=delta,
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

        nutrients = [
            entry
            for entry in feed_program.ec_nutrients
            if entry.enabled and entry.ratio > 0
        ]

        if not nutrients:
            return

        total_ratio = sum(
            entry.ratio
            for entry in nutrients
        )

        for entry in nutrients:

            self._add_action(
                plan=plan,
                system=system,
                nutrient_id=entry.nutrient_id,
                delta=delta,
                ratio=entry.ratio / total_ratio,
                reason="EC correction",
            )

    def _add_action(
        self,
        plan: DosingPlan,
        system: System,
        nutrient_id: str,
        delta: float,
        reason: str,
        ratio: float = 1.0,
    ) -> None:
        """Add a dosing action for a nutrient."""

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

        if nutrient.strength <= 0:
            return

        volume = (
            delta
            * system.water_volume_liters
            / nutrient.strength
        )

        volume *= ratio

        volume = nutrient.clamp_volume(
            volume,
        )

        if volume <= 0:
            return

        plan.add(
            pump_id=pump.id,
            volume_ml=volume,
            runtime_seconds=pump.runtime_for(
                volume,
            ),
            reason=reason,
        )