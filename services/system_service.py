"""Business logic for OpenDoser."""

from __future__ import annotations

from ..exceptions import (
    DuplicateIdError,
    ObjectNotFoundError,
)
from ..model.feed_program import FeedProgram
from ..model.nutrient import Nutrient
from ..model.pump import Pump
from ..model.recipe import Recipe
from ..model.system import System
from ..model.tank import Tank


class SystemService:
    """CRUD operations for the complete system."""

    def __init__(self, system: System) -> None:
        """Initialize the service."""

        self.system = system

    #
    # Pumps
    #

    def create_pump(
        self,
        id: str,
        name: str,
        entity_id: str = "",
    ) -> Pump:
        """Create a pump."""

        if any(p.id == id for p in self.system.pumps):
            raise DuplicateIdError(f"Pump '{id}' already exists.")

        pump = Pump(
            id=id,
            name=name,
            entity_id=entity_id,
        )

        self.system.pumps.append(pump)

        return pump

    def update_pump(
        self,
        id: str,
        name: str,
        entity_id: str,
    ) -> Pump:
        """Update a pump."""

        pump = self.get_pump(id)

        pump.name = name
        pump.entity_id = entity_id

        return pump

    def remove_pump(
        self,
        id: str,
    ) -> None:
        """Remove a pump."""

        pump = self.get_pump(id)

        self.system.pumps.remove(pump)

    def get_pump(
        self,
        id: str,
    ) -> Pump:
        """Return a pump."""

        for pump in self.system.pumps:
            if pump.id == id:
                return pump

        raise ObjectNotFoundError(f"Pump '{id}' not found.")

    #
    # Tanks
    #

    def create_tank(
        self,
        id: str,
        name: str,
        volume: float = 0.0,
    ) -> Tank:
        """Create a tank."""

        if any(t.id == id for t in self.system.tanks):
            raise DuplicateIdError(f"Tank '{id}' already exists.")

        tank = Tank(
            id=id,
            name=name,
            volume=volume,
        )

        self.system.tanks.append(tank)

        return tank

    def update_tank(
        self,
        id: str,
        name: str,
        volume: float,
    ) -> Tank:
        """Update a tank."""

        tank = self.get_tank(id)

        tank.name = name
        tank.volume = volume

        return tank

    def remove_tank(
        self,
        id: str,
    ) -> None:
        """Remove a tank."""

        tank = self.get_tank(id)

        self.system.tanks.remove(tank)

    def get_tank(
        self,
        id: str,
    ) -> Tank:
        """Return a tank."""

        for tank in self.system.tanks:
            if tank.id == id:
                return tank

        raise ObjectNotFoundError(f"Tank '{id}' not found.")

    #
    # Nutrients
    #

    def create_nutrient(
        self,
        id: str,
        name: str,
    ) -> Nutrient:
        """Create a nutrient."""

        if any(n.id == id for n in self.system.nutrients):
            raise DuplicateIdError(f"Nutrient '{id}' already exists.")

        nutrient = Nutrient(
            id=id,
            name=name,
        )

        self.system.nutrients.append(nutrient)

        return nutrient

    def update_nutrient(
        self,
        id: str,
        name: str,
    ) -> Nutrient:
        """Update a nutrient."""

        nutrient = self.get_nutrient(id)

        nutrient.name = name

        return nutrient

    def remove_nutrient(
        self,
        id: str,
    ) -> None:
        """Remove a nutrient."""

        nutrient = self.get_nutrient(id)

        self.system.nutrients.remove(nutrient)

    def get_nutrient(
        self,
        id: str,
    ) -> Nutrient:
        """Return a nutrient."""

        for nutrient in self.system.nutrients:
            if nutrient.id == id:
                return nutrient

        raise ObjectNotFoundError(f"Nutrient '{id}' not found.")

    #
    # Recipes
    #

    def create_recipe(
        self,
        id: str,
        name: str,
    ) -> Recipe:
        """Create a recipe."""

        if any(r.id == id for r in self.system.recipes):
            raise DuplicateIdError(f"Recipe '{id}' already exists.")

        recipe = Recipe(
            id=id,
            name=name,
        )

        self.system.recipes.append(recipe)

        return recipe

    def update_recipe(
        self,
        id: str,
        name: str,
    ) -> Recipe:
        """Update a recipe."""

        recipe = self.get_recipe(id)

        recipe.name = name

        return recipe

    def remove_recipe(
        self,
        id: str,
    ) -> None:
        """Remove a recipe."""

        recipe = self.get_recipe(id)

        self.system.recipes.remove(recipe)

    def get_recipe(
        self,
        id: str,
    ) -> Recipe:
        """Return a recipe."""

        for recipe in self.system.recipes:
            if recipe.id == id:
                return recipe

        raise ObjectNotFoundError(f"Recipe '{id}' not found.")

    #
    # Feed programs
    #

    def create_feed_program(
        self,
        id: str,
        name: str,
    ) -> FeedProgram:
        """Create a feed program."""

        if any(f.id == id for f in self.system.feed_programs):
            raise DuplicateIdError(f"Feed program '{id}' already exists.")

        program = FeedProgram(
            id=id,
            name=name,
        )

        self.system.feed_programs.append(program)

        return program

    def update_feed_program(
        self,
        id: str,
        name: str,
    ) -> FeedProgram:
        """Update a feed program."""

        program = self.get_feed_program(id)

        program.name = name

        return program

    def remove_feed_program(
        self,
        id: str,
    ) -> None:
        """Remove a feed program."""

        program = self.get_feed_program(id)

        self.system.feed_programs.remove(program)

    def get_feed_program(
        self,
        id: str,
    ) -> FeedProgram:
        """Return a feed program."""

        for program in self.system.feed_programs:
            if program.id == id:
                return program

        raise ObjectNotFoundError(f"Feed program '{id}' not found.")