"""OpenDoser correction model."""

from __future__ import annotations

from dataclasses import dataclass, field

from .correction_type import CorrectionType


@dataclass(slots=True)
class Correction:
    """Defines how a recipe performs a correction."""

    type: CorrectionType

    nutrient_ids: list[str] = field(default_factory=list)

    enabled: bool = True