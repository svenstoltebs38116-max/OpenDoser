"""OpenDoser execution result model."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ExecutionResult:
    """Represents the result of executing a dosing plan."""

    completed: bool = False

    cancelled: bool = False

    actions_executed: int = 0

    duration_seconds: float = 0.0

    warnings: list[str] = field(default_factory=list)

    error: str | None = None

    @property
    def successful(self) -> bool:
        """Return True if execution completed successfully."""

        return (
            self.completed
            and not self.cancelled
            and self.error is None
        )

    @property
    def failed(self) -> bool:
        """Return True if execution failed."""

        return self.error is not None

    @property
    def has_warnings(self) -> bool:
        """Return True if warnings are present."""

        return len(self.warnings) > 0

    def add_warning(
        self,
        message: str,
    ) -> None:
        """Add a warning."""

        if message and message not in self.warnings:
            self.warnings.append(message)