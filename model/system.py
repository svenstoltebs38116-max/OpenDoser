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
    # Dosing
    #
    # Waiting time after every dosing action to allow the
    # nutrient solution to mix before the next component
    # is added.
    #

    mix_delay_seconds: float = 180.0

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

    def add_pump(
        self,
        pump: Pump,
    ) -> None:
        """Register a pump."""

        self.pumps[pump.id] = pump

    def add_tank(
        self,
        tank: Tank,
    ) -> None:
        """Register a tank."""

        self.tanks[tank.id] = tank

    def add_nutrient(
        self,
        nutrient: Nutrient,
    ) -> None:
        """Register a nutrient."""

        self.nutrients[nutrient.id] = nutrient

    def add_feed_program(
        self,
        feed_program: FeedProgram,
    ) -> None:
        """Register a feed program."""

        self.feed_programs[feed_program.id] = feed_program

    #
    # Lookup
    #

    def get_pump(
        self,
        pump_id: str,
    ) -> Pump | None:
        """Return a pump."""

        return self.pumps.get(pump_id)

    def get_tank(
        self,
        tank_id: str,
    ) -> Tank | None:
        """Return a tank."""

        return self.tanks.get(tank_id)

    def get_nutrient(
        self,
        nutrient_id: str,
    ) -> Nutrient | None:
        """Return a nutrient."""

        return self.nutrients.get(nutrient_id)

    def get_feed_program(
        self,
        feed_program_id: str,
    ) -> FeedProgram | None:
        """Return a feed program."""

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

    #
    # Serialization
    #

    def to_dict(self) -> dict:
        """Serialize the system."""

        return {
            "recipe": self.recipe.to_dict(),
            "water_volume_liters": self.water_volume_liters,
            "mix_delay_seconds": self.mix_delay_seconds,
            "pumps": [
                pump.to_dict()
                for pump in self.pumps.values()
            ],
            "tanks": [
                tank.to_dict()
                for tank in self.tanks.values()
            ],
            "nutrients": [
                nutrient.to_dict()
                for nutrient in self.nutrients.values()
            ],
            "feed_programs": [
                program.to_dict()
                for program in self.feed_programs.values()
            ],
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> System:
        """Deserialize a system."""

        system = cls(
            recipe=Recipe.from_dict(
                data["recipe"],
            ),
            water_volume_liters=data.get(
                "water_volume_liters",
                100.0,
            ),
            mix_delay_seconds=data.get(
                "mix_delay_seconds",
                180.0,
            ),
        )

        for pump_data in data.get(
            "pumps",
            [],
        ):
            system.add_pump(
                Pump.from_dict(
                    pump_data,
                )
            )

        for tank_data in data.get(
            "tanks",
            [],
        ):
            system.add_tank(
                Tank.from_dict(
                    tank_data,
                )
            )

        for nutrient_data in data.get(
            "nutrients",
            [],
        ):
            system.add_nutrient(
                Nutrient.from_dict(
                    nutrient_data,
                )
            )

        for program_data in data.get(
            "feed_programs",
            [],
        ):
            system.add_feed_program(
                FeedProgram.from_dict(
                    program_data,
                )
            )

        return system