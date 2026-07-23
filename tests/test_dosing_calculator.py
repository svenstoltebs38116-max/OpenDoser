"""Tests for the dosing calculator."""

from custom_components.opendoser.dosing_calculator import DosingCalculator
from custom_components.opendoser.model.nutrient import Nutrient
from custom_components.opendoser.model.nutrient_dose import NutrientDose


def create_nutrient(**kwargs) -> Nutrient:
    """Create a test nutrient."""

    defaults = {
        "id": "test",
        "name": "Test nutrient",
        "pump_id": "pump",
        "enabled": True,
        "strength": 0.1,
        "minimum_dose_ml": 0.0,
        "maximum_dose_ml": 10000.0,
    }

    defaults.update(kwargs)

    return Nutrient(**defaults)


def test_calculate_ph_volume() -> None:
    """Test a normal pH calculation."""

    calculator = DosingCalculator()

    volume = calculator.calculate_ph_volume(
        nutrient=create_nutrient(
            strength=0.05,
        ),
        delta=0.5,
        water_volume_liters=100.0,
    )

    assert volume == 1000.0


def test_zero_delta_returns_zero() -> None:
    """No correction should require no dosing."""

    calculator = DosingCalculator()

    volume = calculator.calculate_ph_volume(
        nutrient=create_nutrient(),
        delta=0.0,
        water_volume_liters=100.0,
    )

    assert volume == 0.0


def test_zero_strength_returns_zero() -> None:
    """A nutrient without strength cannot be dosed."""

    calculator = DosingCalculator()

    volume = calculator.calculate_ph_volume(
        nutrient=create_nutrient(
            strength=0.0,
        ),
        delta=0.5,
        water_volume_liters=100.0,
    )

    assert volume == 0.0


def test_disabled_nutrient_returns_zero() -> None:
    """Disabled nutrients should never be dosed."""

    calculator = DosingCalculator()

    volume = calculator.calculate_ph_volume(
        nutrient=create_nutrient(
            enabled=False,
        ),
        delta=0.5,
        water_volume_liters=100.0,
    )

    assert volume == 0.0


def test_zero_water_volume_returns_zero() -> None:
    """No water volume means no dosing."""

    calculator = DosingCalculator()

    volume = calculator.calculate_ph_volume(
        nutrient=create_nutrient(),
        delta=0.5,
        water_volume_liters=0.0,
    )

    assert volume == 0.0


def test_ec_single_nutrient() -> None:
    """A single nutrient receives the full EC correction."""

    calculator = DosingCalculator()

    volumes = calculator.calculate_ec_volumes(
        nutrient_doses=[
            NutrientDose(
                nutrient=create_nutrient(),
                ratio=1.0,
            ),
        ],
        delta=1.0,
        water_volume_liters=100.0,
    )

    assert len(volumes) == 1
    assert volumes["test"] == 1000.0


def test_ec_ratio_distribution() -> None:
    """Distribute EC correction according to the configured ratios."""

    calculator = DosingCalculator()

    volumes = calculator.calculate_ec_volumes(
        nutrient_doses=[
            NutrientDose(
                nutrient=create_nutrient(
                    id="a",
                ),
                ratio=2.0,
            ),
            NutrientDose(
                nutrient=create_nutrient(
                    id="b",
                ),
                ratio=1.0,
            ),
        ],
        delta=0.9,
        water_volume_liters=100.0,
    )

    assert len(volumes) == 2
    assert volumes["a"] == 600.0
    assert volumes["b"] == 300.0


def test_ec_invalid_ratio_is_ignored() -> None:
    """Nutrients with an invalid ratio should be ignored."""

    calculator = DosingCalculator()

    volumes = calculator.calculate_ec_volumes(
        nutrient_doses=[
            NutrientDose(
                nutrient=create_nutrient(),
                ratio=0.0,
            ),
        ],
        delta=1.0,
        water_volume_liters=100.0,
    )

    assert volumes == {}


def test_ec_disabled_nutrient_is_ignored() -> None:
    """Disabled nutrients should not be dosed."""

    calculator = DosingCalculator()

    volumes = calculator.calculate_ec_volumes(
        nutrient_doses=[
            NutrientDose(
                nutrient=create_nutrient(
                    enabled=False,
                ),
                ratio=1.0,
            ),
        ],
        delta=1.0,
        water_volume_liters=100.0,
    )

    assert volumes == {}


def test_ec_different_strengths() -> None:
    """Different strengths should produce different dosing volumes."""

    calculator = DosingCalculator()

    volumes = calculator.calculate_ec_volumes(
        nutrient_doses=[
            NutrientDose(
                nutrient=create_nutrient(
                    id="a",
                    strength=0.2,
                ),
                ratio=1.0,
            ),
            NutrientDose(
                nutrient=create_nutrient(
                    id="b",
                    strength=0.1,
                ),
                ratio=1.0,
            ),
        ],
        delta=1.0,
        water_volume_liters=100.0,
    )

    assert volumes["a"] == 250.0
    assert volumes["b"] == 500.0