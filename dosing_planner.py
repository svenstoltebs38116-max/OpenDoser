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

        #
        # pH
        #

        if (
            state.ph is not None
            and not recipe.ph_in_range(state.ph)
        ):
            delta = abs(
                recipe.target_ph - state.ph
            )

            nutrient_id = (
                feed_program.ph_up_nutrient_id
                if state.ph < recipe.target_ph
                else feed_program.ph_down_nutrient_id
            )

            if nutrient_id is not None:

                nutrient = system.get_nutrient(
                    nutrient_id,
                )

                if nutrient is not None:

                    pump = system.get_pump(
                        nutrient.pump_id,
                    )

                    if pump is not None:

                        volume = nutrient.required_volume(
                            delta,
                            system.water_volume_liters,
                        )

                        plan.add(
                            pump_id=pump.id,
                            volume_ml=volume,
                            runtime_seconds=pump.runtime_for(
                                volume,
                            ),
                            reason="pH correction",
                        )

        #
        # EC
        #

        if (
            state.ec is not None
            and not recipe.ec_in_range(state.ec)
        ):
            delta = (
                recipe.target_ec
                - state.ec
            )

            if delta > 0:

                for nutrient_id in feed_program.ec_nutrient_ids:

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

                    volume = nutrient.required_volume(
                        delta,
                        system.water_volume_liters,
                    )

                    plan.add(
                        pump_id=pump.id,
                        volume_ml=volume,
                        runtime_seconds=pump.runtime_for(
                            volume,
                        ),
                        reason="EC correction",
                    )

        return plan