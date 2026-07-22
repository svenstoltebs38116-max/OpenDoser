"""OpenDoser feed program model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FeedProgram:
    """Defines how a recipe performs nutrient corrections."""

    id: str
    name: str

    #
    # pH correction
    #

    ph_up_nutrient_id: str | None = None

    ph_down_nutrient_id: str | None = None

    #
    # EC correction
    #

    ec_nutrient_ids: list[str] = field(default_factory=list)

    #
    # General
    #

    enabled: bool = True

    description: str = ""