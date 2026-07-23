"""Calculation result model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class CalculationResult:
    """Represents the result of a dosing calculation."""

    #
    # Final dosing volume after all limits
    # have been applied.
    #

    volume_ml: float

    #
    # Optional warnings generated during
    # the calculation.
    #

    warnings: list[str] = field(
        default_factory=list,
    )

    @property
    def has_warnings(self) -> bool:
        """Return whether warnings exist."""

        return bool(self.warnings)

    def add_warning(
        self,
        warning: str,
    ) -> None:
        """Add a warning if not already present."""

        if warning not in self.warnings:
            self.warnings.append(
                warning,
            )