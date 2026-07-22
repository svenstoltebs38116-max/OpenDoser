"""OpenDoser dosing plan model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DosingAction:
    """Represents a single dosing action."""

    pump_id: str

    volume_ml: float

    reason: str = ""


@dataclass(slots=True)
class DosingPlan:
    """Represents the calculated dosing plan."""

    actions: list[DosingAction] = field(default_factory=list)

    warnings: list[str] = field(default_factory=list)

    def add(
        self,
        pump_id: str,
        volume_ml: float,
        reason: str = "",
    ) -> None:
        """Add a dosing action."""

        if volume_ml <= 0:
            return

        self.actions.append(
            DosingAction(
                pump_id=pump_id,
                volume_ml=volume_ml,
                reason=reason,
            )
        )

    @property
    def empty(self) -> bool:
        """Return True if nothing has to be dosed."""

        return len(self.actions) == 0

    @property
    def total_volume_ml(self) -> float:
        """Return the total dosing volume."""

        return sum(action.volume_ml for action in self.actions)