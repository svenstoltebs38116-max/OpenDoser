"""Tests for DosingPlanner.create_plan()."""

from custom_components.opendoser.dosing_planner import DosingPlanner

from .helpers import (
    create_feed_program,
    create_feed_program_nutrient,
    create_nutrient,
    create_pump,
    create_recipe,
    create_state,
    create_system,
)


def test_create_plan_empty() -> None:
    """Nothing should be dosed when everything is in range."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ph=6.0,
        target_ec=1.6,
    )

    system = create_system(
        recipe=recipe,
    )

    plan = planner.create_plan(
        system=system,
        recipe=recipe,
        feed_program=create_feed_program(),
        state=create_state(
            ph=6.0,
            ec=1.6,
        ),
    )

    assert plan.empty
    assert len(plan.actions) == 0
    assert plan.total_volume_ml == 0
    assert plan.total_runtime_seconds == 0


def test_create_plan_ph_only() -> None:
    """Only a pH correction should be created."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ph=6.0,
        target_ec=1.6,
    )

    pump = create_pump(
        id="pump_ph",
        ml_per_second=2.0,
    )

    nutrient = create_nutrient(
        id="ph_up",
        pump_id="pump_ph",
        strength=0.1,
    )

    system = create_system(
        recipe=recipe,
        pumps=[pump],
        nutrients=[nutrient],
    )

    program = create_feed_program(
        ph_up_nutrient_id="ph_up",
    )

    plan = planner.create_plan(
        system=system,
        recipe=recipe,
        feed_program=program,
        state=create_state(
            ph=5.5,
            ec=1.6,
        ),
    )

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.reason == "pH correction"
    assert action.pump_id == "pump_ph"
    assert action.volume_ml > 0
    assert action.runtime_seconds > 0


def test_create_plan_ec_only() -> None:
    """Only EC corrections should be created."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ec=2.0,
    )

    pump = create_pump(
        id="pump_a",
    )

    nutrient = create_nutrient(
        id="grow_a",
        pump_id="pump_a",
        strength=0.1,
    )

    system = create_system(
        recipe=recipe,
        pumps=[pump],
        nutrients=[nutrient],
    )

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="grow_a",
            ),
        ],
    )

    plan = planner.create_plan(
        system=system,
        recipe=recipe,
        feed_program=program,
        state=create_state(
            ph=recipe.target_ph,
            ec=1.0,
        ),
    )

    assert len(plan.actions) == 1

    action = plan.actions[0]

    assert action.reason == "EC correction"
    assert action.pump_id == "pump_a"
    assert action.volume_ml > 0
    assert action.runtime_seconds > 0


def test_create_plan_ph_and_ec() -> None:
    """pH and EC corrections should both be included."""

    planner = DosingPlanner()

    recipe = create_recipe(
        target_ph=6.0,
        target_ec=2.0,
    )

    ph_pump = create_pump(
        id="pump_ph",
    )

    ec_pump = create_pump(
        id="pump_ec",
    )

    ph_nutrient = create_nutrient(
        id="ph_up",
        pump_id="pump_ph",
        strength=0.1,
    )

    ec_nutrient = create_nutrient(
        id="grow",
        pump_id="pump_ec",
        strength=0.1,
    )

    system = create_system(
        recipe=recipe,
        pumps=[
            ph_pump,
            ec_pump,
        ],
        nutrients=[
            ph_nutrient,
            ec_nutrient,
        ],
    )

    program = create_feed_program(
        ph_up_nutrient_id="ph_up",
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="grow",
            ),
        ],
    )

    plan = planner.create_plan(
        system=system,
        recipe=recipe,
        feed_program=program,
        state=create_state(
            ph=5.5,
            ec=1.0,
        ),
    )

    assert len(plan.actions) == 2

    reasons = {
        action.reason
        for action in plan.actions
    }

    assert reasons == {
        "pH correction",
        "EC correction",
    }

    assert plan.total_volume_ml > 0
    assert plan.total_runtime_seconds > 0