"""OpenDoser feed program model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .feed_program_nutrient import FeedProgramNutrient


@dataclass(slots=True)
class FeedProgram:
    """Defines how a recipe performs nutrient corrections."""

    #
    # Identity
    #

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

    ec_nutrients: list[FeedProgramNutrient] = field(
        default_factory=list,
    )

    #
    # General
    #

    enabled: bool = True

    description: str = ""

    def to_dict(self) -> dict:
        """Serialize the feed program."""

        return {
            "id": self.id,
            "name": self.name,
            "ph_up_nutrient_id": self.ph_up_nutrient_id,
            "ph_down_nutrient_id": self.ph_down_nutrient_id,
            "ec_nutrients": [
                nutrient.to_dict()
                for nutrient in self.ec_nutrients
            ],
            "enabled": self.enabled,
            "description": self.description,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> "FeedProgram":
        """Deserialize a feed program."""

        return cls(
            id=data["id"],
            name=data["name"],
            ph_up_nutrient_id=data.get(
                "ph_up_nutrient_id",
            ),
            ph_down_nutrient_id=data.get(
                "ph_down_nutrient_id",
            ),
            ec_nutrients=[
                FeedProgramNutrient.from_dict(item)
                for item in data.get(
                    "ec_nutrients",
                    [],
                )
            ],
            enabled=data.get(
                "enabled",
                True,
            ),
            description=data.get(
                "description",
                "",
            ),
        )