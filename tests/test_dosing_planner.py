"""Tests for the dosing planner."""

from custom_components.opendoser.dosing_planner import DosingPlanner

from .helpers import (
    create_feed_program,
    create_feed_program_nutrient,
    create_nutrient,
    create_pump,
    create_system,
)


def test_create_nutrient_doses_empty() -> None:
    """An empty feed program should produce no nutrient doses."""

    planner = DosingPlanner()

    system = create_system()

    program = create_feed_program()

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert doses == []


def test_invalid_entries_are_ignored() -> None:
    """Disabled feed program entries should be ignored."""

    planner = DosingPlanner()

    pump = create_pump(id="pump_a")

    nutrient = create_nutrient(
        id="a",
        pump_id="pump_a",
    )

    system = create_system(
        pumps=[pump],
        nutrients=[nutrient],
    )

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="a",
                enabled=False,
            ),
        ],
    )

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert doses == []


def test_unknown_nutrient_is_ignored() -> None:
    """Unknown nutrients should be ignored."""

    planner = DosingPlanner()

    system = create_system()

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="unknown",
            ),
        ],
    )

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert doses == []


def test_entries_are_sorted_by_priority() -> None:
    """Entries should be sorted by priority."""

    planner = DosingPlanner()

    pumps = [
        create_pump(id="pump_a"),
        create_pump(id="pump_b"),
        create_pump(id="pump_c"),
    ]

    nutrients = [
        create_nutrient(
            id="a",
            pump_id="pump_a",
        ),
        create_nutrient(
            id="b",
            pump_id="pump_b",
        ),
        create_nutrient(
            id="c",
            pump_id="pump_c",
        ),
    ]

    system = create_system(
        pumps=pumps,
        nutrients=nutrients,
    )

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="c",
                priority=3,
            ),
            create_feed_program_nutrient(
                nutrient_id="a",
                priority=1,
            ),
            create_feed_program_nutrient(
                nutrient_id="b",
                priority=2,
            ),
        ],
    )

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert [dose.nutrient.id for dose in doses] == [
        "a",
        "b",
        "c",
    ]


def test_ratio_is_preserved() -> None:
    """The configured ratio should be preserved."""

    planner = DosingPlanner()

    pump = create_pump(id="pump_a")

    nutrient = create_nutrient(
        id="a",
        pump_id="pump_a",
    )

    system = create_system(
        pumps=[pump],
        nutrients=[nutrient],
    )

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="a",
                ratio=2.5,
            ),
        ],
    )

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert len(doses) == 1
    assert doses[0].ratio == 2.5


def test_correct_nutrient_object_is_used() -> None:
    """The returned Nutrient object should be used."""

    planner = DosingPlanner()

    pump = create_pump(id="pump_b")

    nutrient = create_nutrient(
        id="b",
        pump_id="pump_b",
    )

    system = create_system(
        pumps=[pump],
        nutrients=[nutrient],
    )

    program = create_feed_program(
        ec_nutrients=[
            create_feed_program_nutrient(
                nutrient_id="b",
            ),
        ],
    )

    doses = planner._create_nutrient_doses(
        system,
        program,
    )

    assert len(doses) == 1
    assert doses[0].nutrient is nutrient