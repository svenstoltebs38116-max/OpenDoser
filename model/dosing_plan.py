"""OpenDoser dosing plan model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DosingAction:
    """Represents a single dosing action."""

    pump_id: str

    volume_ml: float

    runtime_seconds: float = 0.0

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
        runtime_seconds: float = 0.0,
        reason: str = "",
    ) -> None:
        """Add a dosing action."""

        if volume_ml <= 0:
            return

        self.actions.append(
            DosingAction(
                pump_id=pump_id,
                volume_ml=volume_ml,
                runtime_seconds=runtime_seconds,
                reason=reason,
            )
        )

    def add_warning(
        self,
        message: str,
    ) -> None:
        """Add a warning."""

        if message:
            self.warnings.append(message)

    @property
    def empty(self) -> bool:
        """Return True if nothing has to be dosed."""

        return not self.actions

    @property
    def total_volume_ml(self) -> float:
        """Return the total dosing volume."""

        return sum(
            action.volume_ml
            for action in self.actions
        )

    @property
    def total_runtime_seconds(self) -> float:
        """Return the total runtime."""

        return sum(
            action.runtime_seconds
            for action in self.actions
        )