"""OpenDoser dosing calculator."""

from __future__ import annotations

from .model.dosing_plan import DosingPlan
from .model.nutrient import Nutrient
from .model.system import System
from .model.system_state import SystemState


class DosingCalculator:
    """Calculates dosing requirements."""

    def calculate(
        self,
        system: System,
        state: SystemState,
    ) -> DosingPlan:
        """Calculate a dosing plan."""

        plan = DosingPlan()

        recipe = system.recipe

        if not recipe.enabled:
            plan.warnings.append("Recipe is disabled.")
            return plan

        if not state.available:
            plan.warnings.append("Required sensors unavailable.")
            return plan

        #
        # EC calculation
        #

        if state.ec < recipe.target_ec:

            delta = recipe.target_ec - state.ec

            for nutrient in system.nutrients.values():

                if nutrient.id != "ec":
                    continue

                volume = nutrient.required_volume(
                    delta=delta,
                    water_volume_liters=system.water_volume_liters,
                )

                if volume > 0:

                    plan.add(
                        pump_id=nutrient.pump_id,
                        volume_ml=volume,
                        reason=f"Increase EC by {delta:.2f}",
                    )

        #
        # pH calculation
        #

        if state.ph > recipe.target_ph:

            delta = state.ph - recipe.target_ph

            for nutrient in system.nutrients.values():

                if nutrient.id != "ph_down":
                    continue

                volume = nutrient.required_volume(
                    delta=delta,
                    water_volume_liters=system.water_volume_liters,
                )

                if volume > 0:

                    plan.add(
                        pump_id=nutrient.pump_id,
                        volume_ml=volume,
                        reason=f"Lower pH by {delta:.2f}",
                    )

        return plan