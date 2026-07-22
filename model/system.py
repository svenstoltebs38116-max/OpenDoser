"""OpenDoser system model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .feed_program import FeedProgram
from .nutrient import Nutrient
from .pump import Pump
from .recipe import Recipe
from .tank import Tank


@dataclass(slots=True)
class System:
    """Represents a complete OpenDoser installation."""

    #
    # Recipe
    #

    recipe: Recipe

    #
    # Water
    #

    water_volume_liters: float = 100.0

    #
    # Hardware
    #

    pumps: dict[str, Pump] = field(default_factory=dict)

    tanks: dict[str, Tank] = field(default_factory=dict)

    nutrients: dict[str, Nutrient] = field(default_factory=dict)

    feed_programs: dict[str, FeedProgram] = field(default_factory=dict)

    #
    # Registration
    #

    def add_pump(self, pump: Pump) -> None:
        """Register a pump."""

        self.pumps[pump.id] = pump

    def add_tank(self, tank: Tank) -> None:
        """Register a tank."""

        self.tanks[tank.id] = tank

    def add_nutrient(self, nutrient: Nutrient) -> None:
        """Register a nutrient."""

        self.nutrients[nutrient.id] = nutrient

    def add_feed_program(self, feed_program: FeedProgram) -> None:
        """Register a feed program."""

        self.feed_programs[feed_program.id] = feed_program

    #
    # Lookup
    #

    def get_pump(self, pump_id: str) -> Pump | None:
        """Return a pump."""

        return self.pumps.get(pump_id)

    def get_tank(self, tank_id: str) -> Tank | None:
        """Return a tank."""

        return self.tanks.get(tank_id)

    def get_nutrient(self, nutrient_id: str) -> Nutrient | None:
        """Return a nutrient by id."""

        return self.nutrients.get(nutrient_id)

    def get_feed_program(
        self,
        feed_program_id: str,
    ) -> FeedProgram | None:
        """Return a feed program by id."""

        return self.feed_programs.get(feed_program_id)

    #
    # Convenience
    #

    @property
    def enabled_pumps(self) -> list[Pump]:
        """Return all enabled pumps."""

        return [
            pump
            for pump in self.pumps.values()
            if pump.enabled
        ]

    @property
    def enabled_tanks(self) -> list[Tank]:
        """Return all enabled tanks."""

        return [
            tank
            for tank in self.tanks.values()
            if tank.enabled
        ]

    @property
    def enabled_nutrients(self) -> list[Nutrient]:
        """Return all enabled nutrients."""

        return [
            nutrient
            for nutrient in self.nutrients.values()
            if nutrient.enabled
        ]

    @property
    def enabled_feed_programs(self) -> list[FeedProgram]:
        """Return all enabled feed programs."""

        return [
            program
            for program in self.feed_programs.values()
            if program.enabled
        ]