"""OpenDoser business logic."""

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
        # Feed program
        #

        feed_program = None

        if system.recipe.feed_program_id is not None:
            feed_program = system.get_feed_program(
                system.recipe.feed_program_id,
            )

        #
        # pH evaluation
        #

        if (
            feed_program is not None
            and state.ph is not None
            and not system.recipe.ph_in_range(state.ph)
        ):
            plan.warnings.append(
                f"pH {state.ph:.2f} "
                f"(target {system.recipe.target_ph:.2f})"
            )

            delta = abs(system.recipe.target_ph - state.ph)

            if state.ph < system.recipe.target_ph:
                nutrient_id = feed_program.ph_up_nutrient_id
            else:
                nutrient_id = feed_program.ph_down_nutrient_id

            if nutrient_id is not None:
                nutrient = system.get_nutrient(nutrient_id)

                if nutrient is not None:
                    plan.add(
                        nutrient=nutrient,
                        volume_ml=nutrient.required_volume(
                            delta,
                            system.water_volume_liters,
                        ),
                    )

        #
        # EC evaluation
        #

        if (
            feed_program is not None
            and state.ec is not None
            and not system.recipe.ec_in_range(state.ec)
        ):
            plan.warnings.append(
                f"EC {state.ec:.2f} "
                f"(target {system.recipe.target_ec:.2f})"
            )

            delta = system.recipe.target_ec - state.ec

            #
            # Only dose if EC is below target
            #

            if delta > 0:

                for nutrient_id in feed_program.ec_nutrient_ids:

                    nutrient = system.get_nutrient(
                        nutrient_id,
                    )

                    if nutrient is None:
                        continue

                    plan.add(
                        nutrient=nutrient,
                        volume_ml=nutrient.required_volume(
                            delta,
                            system.water_volume_liters,
                        ),
                    )

        return plan