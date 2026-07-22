"""OpenDoser business logic. TEST"""

from __future__ import annotations

from .model.dosing_plan import DosingPlan
from .model.system import System
from .model.system_state import SystemState


class OpenDoserEngine:
    """Business logic layer for OpenDoser."""

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
            plan.warnings.append("Recipe is disabled.")
            return plan

        #
        # Required sensors available?
        #

        if not state.available:
            plan.warnings.append("Required sensors unavailable.")
            return plan

        #
        # pH evaluation
        #

        if state.ph is not None and not system.recipe.ph_in_range(state.ph):
            plan.warnings.append(
                f"pH {state.ph:.2f} "
                f"(target {system.recipe.target_ph:.2f})"
            )

            nutrient = system.get_nutrient("ph_down")
            if nutrient is not None:
                plan.add(
                    nutrient=nutrient,
                    volume_ml=nutrient.required_volume(
                        system.water_volume_liters,
                    ),
                )

        #
        # EC evaluation
        #

        if state.ec is not None and not system.recipe.ec_in_range(state.ec):
            plan.warnings.append(
                f"EC {state.ec:.2f} "
                f"(target {system.recipe.target_ec:.2f})"
            )

            nutrient = system.get_nutrient("ec")
            if nutrient is not None:
                plan.add(
                    nutrient=nutrient,
                    volume_ml=nutrient.required_volume(
                        system.water_volume_liters,
                    ),
                )

        return plan