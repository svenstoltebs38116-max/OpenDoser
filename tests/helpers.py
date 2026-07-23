"""Shared test helpers."""

from custom_components.opendoser.model.feed_program import FeedProgram
from custom_components.opendoser.model.feed_program_nutrient import (
    FeedProgramNutrient,
)
from custom_components.opendoser.model.nutrient import Nutrient
from custom_components.opendoser.model.pump import Pump
from custom_components.opendoser.model.recipe import Recipe
from custom_components.opendoser.model.system import System
from custom_components.opendoser.model.system_state import SystemState


def create_recipe(**kwargs) -> Recipe:
    """Create a recipe."""

    defaults = {
        "id": "recipe",
        "name": "Recipe",
        "target_ph": 6.0,
        "target_ec": 1.6,
        "ph_tolerance": 0.1,
        "ec_tolerance": 0.05,
        "enabled": True,
    }

    defaults.update(kwargs)

    return Recipe(**defaults)


def create_pump(**kwargs) -> Pump:
    """Create a pump."""

    defaults = {
        "id": "pump",
        "name": "Pump",
        "entity_id": "switch.pump",
        "ml_per_second": 1.0,
        "calibration_factor": 1.0,
        "enabled": True,
    }

    defaults.update(kwargs)

    return Pump(**defaults)


def create_nutrient(**kwargs) -> Nutrient:
    """Create a nutrient."""

    defaults = {
        "id": "nutrient",
        "name": "Nutrient",
        "pump_id": "pump",
        "strength": 0.1,
        "minimum_dose_ml": 0.0,
        "maximum_dose_ml": 1000.0,
        "enabled": True,
    }

    defaults.update(kwargs)

    return Nutrient(**defaults)


def create_feed_program_nutrient(**kwargs) -> FeedProgramNutrient:
    """Create a feed program nutrient."""

    defaults = {
        "nutrient_id": "nutrient",
        "ratio": 1.0,
        "priority": 1,
        "enabled": True,
    }

    defaults.update(kwargs)

    return FeedProgramNutrient(**defaults)


def create_feed_program(**kwargs) -> FeedProgram:
    """Create a feed program."""

    defaults = {
        "id": "program",
        "name": "Program",
        "enabled": True,
        "ph_up_nutrient_id": None,
        "ph_down_nutrient_id": None,
        "ec_nutrients": [],
    }

    defaults.update(kwargs)

    return FeedProgram(**defaults)


def create_state(**kwargs) -> SystemState:
    """Create a system state."""

    defaults = {
        "ph": 6.0,
        "ec": 1.6,
        "temperature": 20.0,
    }

    defaults.update(kwargs)

    return SystemState(**defaults)


def create_system(**kwargs) -> System:
    """Create a system."""

    recipe = kwargs.pop(
        "recipe",
        create_recipe(),
    )

    water_volume = kwargs.pop(
        "water_volume_liters",
        100.0,
    )

    system = System(
        recipe=recipe,
        water_volume_liters=water_volume,
    )

    for pump in kwargs.pop("pumps", []):
        system.add_pump(pump)

    for nutrient in kwargs.pop("nutrients", []):
        system.add_nutrient(nutrient)

    for program in kwargs.pop("feed_programs", []):
        system.add_feed_program(program)

    return system