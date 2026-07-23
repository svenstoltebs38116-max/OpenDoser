"""OpenDoser schedule entry model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ScheduleEntry:
    """Defines one execution schedule."""

    #
    # Identity
    #

    id: str
    name: str

    #
    # References
    #

    recipe_id: str
    feed_program_id: str

    #
    # Time
    #

    enabled: bool = True

    start_time: str = "08:00"

    interval_minutes: int = 30

    #
    # Weekdays
    #

    weekdays: list[int] = field(
        default_factory=lambda: [
            0,
            1,
            2,
            3,
            4,
            5,
            6,
        ],
    )

    #
    # Conditions
    #

    only_if_outside_tolerance: bool = True

    #

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "name": self.name,
            "recipe_id": self.recipe_id,
            "feed_program_id": self.feed_program_id,
            "enabled": self.enabled,
            "start_time": self.start_time,
            "interval_minutes": self.interval_minutes,
            "weekdays": list(self.weekdays),
            "only_if_outside_tolerance": self.only_if_outside_tolerance,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "ScheduleEntry":

        return cls(
            id=data["id"],
            name=data["name"],
            recipe_id=data["recipe_id"],
            feed_program_id=data["feed_program_id"],
            enabled=data.get(
                "enabled",
                True,
            ),
            start_time=data.get(
                "start_time",
                "08:00",
            ),
            interval_minutes=data.get(
                "interval_minutes",
                30,
            ),
            weekdays=list(
                data.get(
                    "weekdays",
                    [
                        0,
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                    ],
                ),
            ),
            only_if_outside_tolerance=data.get(
                "only_if_outside_tolerance",
                True,
            ),
        )