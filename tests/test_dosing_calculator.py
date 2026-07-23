"""Tests for the dosing calculator."""

from custom_components.opendoser.dosing_calculator import DosingCalculator
from custom_components.opendoser.model.nutrient import Nutrient


def create_nutrient(
    strength: float = 0.1,
    enabled: bool = True,
) -> Nutrient:
    """Create a test nutrient."""

    return Nutrient(
        id="test",
        name="Test nutrient",
        pump_id="pump",
        enabled=enabled,
        strength=strength,
        minimum_dose_ml=0.0,
        maximum_dose_ml=10000.0,
    )


def test_calculate_ph_volume() -> None:
    """Test a normal pH calculation."""

    calculator = DosingCalculator()

    nutrient = create_nutrient(
        strength=0.05,
    )

    volume = calculator.calculate_ph_volume(
        nutrient=nutrient,
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