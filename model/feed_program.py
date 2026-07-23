"""OpenDoser feed program model."""

from __future__ import annotations

from dataclasses import dataclass, field


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

    ec_nutrient_ids: list[str] = field(default_factory=list)

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
            "ec_nutrient_ids": list(self.ec_nutrient_ids),
            "enabled": self.enabled,
            "description": self.description,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> FeedProgram:
        """Deserialize a feed program."""

        return cls(
            id=data["id"],
            name=data["name"],
            ph_up_nutrient_id=data.get("ph_up_nutrient_id"),
            ph_down_nutrient_id=data.get("ph_down_nutrient_id"),
            ec_nutrient_ids=list(
                data.get("ec_nutrient_ids", []),
            ),
            enabled=data.get(
                "enabled",
                True,
            ),
            description=data.get(
                "description",
                "",
            ),
        )