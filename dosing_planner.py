"""OpenDoser dosing planner."""

from __future__ import annotations

from .dosing_calculator import DosingCalculator
from .model.dosing_plan import DosingPlan
from .model.feed_program import FeedProgram
from .model.nutrient_dose import NutrientDose
from .model.recipe import Recipe
from .model.system import System
from .model.system_state import SystemState
from .roles import Role


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

        delta = abs(recipe.target_ph - state.ph)

        nutrient_id = (
            feed_program.ph_up_nutrient_id
            if state.ph < recipe.target_ph
            else feed_program.ph_down_nutrient_id
        )

        if nutrient_id is None:
            return

        nutrient = system.get_nutrient(nutrient_id)

        if nutrient is None:
            return

        pump = system.get_pump(nutrient.pump_id)

        if pump is None:
            return

        result = self._calculator.calculate_ph_volume(
            nutrient=nutrient,
            delta=delta,
            water_volume_liters=system.water_volume_liters,
        )

        volume = result.volume_ml

        if volume <= 0:
            return

        role = (
            Role.PH_UP_PUMP
            if state.ph < recipe.target_ph
            else Role.PH_DOWN_PUMP
        )

        plan.add(
            role=role,
            volume_ml=volume,
            runtime_seconds=pump.runtime_for(volume),
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

        nutrient_doses = self._create_nutrient_doses(
            system,
            feed_program,
        )

        if not nutrient_doses:
            return

        volumes = self._calculator.calculate_ec_volumes(
            nutrient_doses=nutrient_doses,
            delta=delta,
            water_volume_liters=system.water_volume_liters,
        )

        for nutrient_id, result in volumes.items():

            nutrient = system.get_nutrient(nutrient_id)

            if nutrient is None:
                continue

            pump = system.get_pump(nutrient.pump_id)

            if pump is None:
                continue

            role = self._ec_role_for_pump(pump.id)

            if role is None:
                continue

            volume = result.volume_ml

            if volume <= 0:
                continue

            plan.add(
                role=role,
                volume_ml=volume,
                runtime_seconds=pump.runtime_for(volume),
                reason="EC correction",
            )

    def _create_nutrient_doses(
        self,
        system: System,
        feed_program: FeedProgram,
    ) -> list[NutrientDose]:
        """Create nutrient doses from the feed program."""

        doses: list[NutrientDose] = []

        nutrients = sorted(
            (
                entry
                for entry in feed_program.ec_nutrients
                if entry.valid
            ),
            key=lambda entry: entry.priority,
        )

        for entry in nutrients:

            nutrient = system.get_nutrient(
                entry.nutrient_id,
            )

            if nutrient is None:
                continue

            doses.append(
                NutrientDose(
                    nutrient=nutrient,
                    ratio=entry.ratio,
                )
            )

        return doses

    @staticmethod
    def _ec_role_for_pump(
        pump_id: str,
    ) -> Role | None:
        """Map an EC pump ID to its logical role."""

        mapping = {
            "ec_a": Role.EC_A_PUMP,
            "ec_b": Role.EC_B_PUMP,
        }

        return mapping.get(pump_id)