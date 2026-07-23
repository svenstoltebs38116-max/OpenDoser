"""OpenDoser configuration."""

from __future__ import annotations

from .model.feed_program import FeedProgram
from .model.feed_program_nutrient import FeedProgramNutrient
from .model.nutrient import Nutrient
from .model.pump import Pump
from .model.recipe import Recipe
from .model.system import System


class Configuration:
    """OpenDoser configuration."""

    @classmethod
    def create_default_system(cls) -> System:
        """Create a default system."""

        recipe = cls.create_default_recipe()

        system = System(recipe=recipe)

        #
        # Hardware
        #

        for pump in cls.create_default_pumps():
            system.add_pump(pump)

        #
        # Nutrients
        #

        for nutrient in cls.create_default_nutrients():
            system.add_nutrient(nutrient)

        #
        # Feed programs
        #

        for program in cls.create_default_feed_programs():
            system.add_feed_program(program)

        return system

    @staticmethod
    def create_default_recipe() -> Recipe:
        """Create the default recipe."""

        return Recipe(
            id="default",
            name="Default Recipe",
            feed_program_id="default",
        )

    @staticmethod
    def create_default_pumps() -> list[Pump]:
        """Create default pumps."""

        return [
            Pump(
                id="pump_ph_down",
                name="pH Down Pump",
                entity_id="switch.ph_down_pump",
            ),
            Pump(
                id="pump_ec",
                name="EC Pump",
                entity_id="switch.ec_pump",
            ),
        ]

    @staticmethod
    def create_default_nutrients() -> list[Nutrient]:
        """Create default nutrients."""

        return [
            Nutrient(
                id="ph_down",
                name="pH Down",
                pump_id="pump_ph_down",
                tank_id="tank_ph_down",
                strength=0.05,
            ),
            Nutrient(
                id="ec",
                name="EC",
                pump_id="pump_ec",
                tank_id="tank_ec",
                strength=0.10,
            ),
        ]

    @staticmethod
    def create_default_feed_programs() -> list[FeedProgram]:
        """Create default feed programs."""

        return [
            FeedProgram(
                id="default",
                name="Default Feed Program",
                ph_up_nutrient_id=None,
                ph_down_nutrient_id="ph_down",
                ec_nutrients=[
                    FeedProgramNutrient(
                        nutrient_id="ec",
                        ratio=1.0,
                    ),
                ],
            )
        ]