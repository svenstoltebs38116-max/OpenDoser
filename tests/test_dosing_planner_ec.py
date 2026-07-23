"""Tests for the EC planning of the dosing planner."""

from custom_components.opendoser.dosing_planner import DosingPlanner
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


def test_plan_ec_in_range_creates_no_action() -> None:
    """No EC correction should be created when already in range."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=1.60,
    )

    system = create_system(
        recipe=recipe,
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(),
        state=create_state(
            ec=1.61,
        ),
    )

    assert plan.empty


def test_plan_ec_above_target_creates_no_action() -> None:
    """No correction should be created when EC is above target."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=1.60,
    )

    system = create_system(
        recipe=recipe,
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(),
        state=create_state(
            ec=2.00,
        ),
    )

    assert plan.empty


def test_plan_ec_without_nutrients_creates_no_action() -> None:
    """No correction should be created without configured nutrients."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    system = create_system(
        recipe=recipe,
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(),
        state=create_state(
            ec=1.00,
        ),
    )

    assert plan.empty


def test_plan_ec_unknown_nutrient_creates_no_action() -> None:
    """Unknown nutrients should be ignored."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    system = create_system(
        recipe=recipe,
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(
            ec_nutrients=[
                create_feed_program_nutrient(
                    nutrient_id="unknown",
                ),
            ],
        ),
        state=create_state(
            ec=1.00,
        ),
    )

    assert plan.empty


def test_plan_ec_missing_pump_creates_no_action() -> None:
    """Missing pumps should be ignored."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    nutrient = create_nutrient(
        id="grow",
        pump_id="pump_grow",
        strength=0.10,
    )

    system = create_system(
        recipe=recipe,
        nutrients=[nutrient],
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(
            ec_nutrients=[
                create_feed_program_nutrient(
                    nutrient_id="grow",
                ),
            ],
        ),
        state=create_state(
            ec=1.00,
        ),
    )

    assert plan.empty


def test_plan_ec_single_nutrient_creates_action() -> None:
    """A single nutrient should create one dosing action."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    pump = create_pump(
        id="pump_grow",
        ml_per_second=2.0,
    )

    nutrient = create_nutrient(
        id="grow",
        pump_id="pump_grow",
        strength=0.10,
    )

    system = create_system(
        recipe=recipe,
        pumps=[pump],
        nutrients=[nutrient],
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(
            ec_nutrients=[
                create_feed_program_nutrient(
                    nutrient_id="grow",
                ),
            ],
        ),
        state=create_state(
            ec=1.00,
        ),
    )

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.pump_id == "pump_grow"
    assert action.volume_ml > 0
    assert action.runtime_seconds > 0
    assert action.reason == "EC correction"


def test_plan_ec_multiple_nutrients_create_multiple_actions() -> None:
    """Multiple nutrients should create multiple actions."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    pump_a = create_pump(
        id="pump_a",
    )

    pump_b = create_pump(
        id="pump_b",
    )

    nutrient_a = create_nutrient(
        id="a",
        pump_id="pump_a",
        strength=0.10,
    )

    nutrient_b = create_nutrient(
        id="b",
        pump_id="pump_b",
        strength=0.10,
    )

    system = create_system(
        recipe=recipe,
        pumps=[
            pump_a,
            pump_b,
        ],
        nutrients=[
            nutrient_a,
            nutrient_b,
        ],
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(
            ec_nutrients=[
                create_feed_program_nutrient(
                    nutrient_id="a",
                    priority=1,
                ),
                create_feed_program_nutrient(
                    nutrient_id="b",
                    priority=2,
                ),
            ],
        ),
        state=create_state(
            ec=1.00,
        ),
    )

    assert len(plan.actions) == 2

    assert plan.actions[0].pump_id == "pump_a"
    assert plan.actions[1].pump_id == "pump_b"


def test_plan_ec_total_volume_is_positive() -> None:
    """The total dosing volume should be greater than zero."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.00,
    )

    pump = create_pump(
        id="pump",
    )

    nutrient = create_nutrient(
        id="grow",
        pump_id="pump",
        strength=0.10,
    )

    system = create_system(
        recipe=recipe,
        pumps=[pump],
        nutrients=[nutrient],
    )

    plan = DosingPlan()

    planner._plan_ec(
        plan=plan,
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(
            ec_nutrients=[
                create_feed_program_nutrient(
                    nutrient_id="grow",
                ),
            ],
        ),
        state=create_state(
            ec=1.00,
        ),
    )

    assert plan.total_volume_ml > 0
    assert plan.total_runtime_seconds > 0