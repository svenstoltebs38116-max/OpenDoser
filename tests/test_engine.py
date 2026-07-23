"""Tests for the OpenDoser engine."""

from custom_components.opendoser.engine import OpenDoserEngine
from custom_components.opendoser.model.dosing_plan import DosingPlan

from .helpers import (
    create_feed_program,
    create_feed_program_nutrient,
    create_nutrient,
    create_pump,
    create_recipe,
    create_state,
    create_system,
)


def test_validate_returns_no_warnings() -> None:
    """A valid configuration should return no warnings."""

    recipe = create_recipe(
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
        feed_programs=[
            create_feed_program(id="program"),
        ],
    )

    state = create_state()

    engine = OpenDoserEngine()

    warnings = engine.validate(
        system=system,
        state=state,
    )

    assert warnings == []


def test_validate_disabled_recipe() -> None:
    """A disabled recipe should produce a warning."""

    recipe = create_recipe(
        enabled=False,
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    warnings = engine.validate(
        system=system,
        state=create_state(),
    )

    assert "Recipe is disabled." in warnings


def test_validate_missing_sensors() -> None:
    """Missing sensors should produce a warning."""

    recipe = create_recipe(
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
    )

    state = create_state(
        temperature=None,
    )

    engine = OpenDoserEngine()

    warnings = engine.validate(
        system=system,
        state=state,
    )

    assert "Required sensors unavailable." in warnings


def test_validate_missing_feed_program() -> None:
    """Missing feed program selection should produce a warning."""

    recipe = create_recipe(
        feed_program_id=None,
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    warnings = engine.validate(
        system=system,
        state=create_state(),
    )

    assert "No feed program selected." in warnings


def test_get_feed_program_none() -> None:
    """No configured feed program should return None."""

    recipe = create_recipe(
        feed_program_id=None,
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    assert engine.get_feed_program(system) is None


def test_get_feed_program_found() -> None:
    """The configured feed program should be returned."""

    program = create_feed_program(
        id="program",
    )

    recipe = create_recipe(
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
        feed_programs=[program],
    )

    engine = OpenDoserEngine()

    assert engine.get_feed_program(system) is program


def test_get_feed_program_missing() -> None:
    """Unknown feed programs should return None."""

    recipe = create_recipe(
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    assert engine.get_feed_program(system) is None


def test_calculate_returns_warning_plan() -> None:
    """Validation warnings should stop planning."""

    recipe = create_recipe(
        enabled=False,
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    plan = engine.calculate(
        system=system,
        state=create_state(),
    )

    assert isinstance(plan, DosingPlan)
    assert plan.has_warnings
    assert plan.empty


def test_calculate_feed_program_not_found() -> None:
    """Missing feed program should return a warning."""

    recipe = create_recipe(
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
    )

    engine = OpenDoserEngine()

    plan = engine.calculate(
        system=system,
        state=create_state(),
    )

    assert plan.has_warnings
    assert "Feed program not found." in plan.warnings


def test_calculate_returns_dosing_plan() -> None:
    """A valid configuration should create a dosing plan."""

    pump = create_pump(
        id="pump_a",
    )

    nutrient = create_nutrient(
        id="grow",
        pump_id="pump_a",
        strength=0.1,
    )

    program = create_feed_program(
        id="program",
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="grow",
            ),
        ],
    )

    recipe = create_recipe(
        target_ec=2.0,
        feed_program_id="program",
    )

    system = create_system(
        recipe=recipe,
        pumps=[pump],
        nutrients=[nutrient],
        feed_programs=[program],
    )

    state = create_state(
        ec=1.0,
    )

    engine = OpenDoserEngine()

    plan = engine.calculate(
        system=system,
        state=state,
    )

    assert not plan.has_warnings
    assert len(plan.actions) == 1
    assert plan.actions[0].reason == "EC correction"
    assert plan.total_volume_ml > 0