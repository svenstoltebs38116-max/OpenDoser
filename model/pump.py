"""OpenDoser pump model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Pump:
    """Represents a dosing pump."""

    #
    # Identity
    #

    id: str
    name: str

    #
    # Home Assistant
    #

    entity_id: str = ""

    #
    # Calibration
    #

    ml_per_second: float = 1.0

    calibration_factor: float = 1.0

    calibrated: bool = False

    last_calibration: str | None = None

    #
    # Limits
    #

    minimum_dose_ml: float = 0.5

    maximum_dose_ml: float = 100.0

    #
    # General
    #

    enabled: bool = True

    @property
    def effective_flow_rate(self) -> float:
        """Return the calibrated flow rate."""

        return self.ml_per_second * self.calibration_factor

    def runtime_for(
        self,
        volume_ml: float,
    ) -> float:
        """Return the runtime in seconds."""

        if volume_ml <= 0:
            return 0.0

        flow = self.effective_flow_rate

        if flow <= 0:
            return 0.0

        return volume_ml / flow

    def can_dose(
        self,
        volume_ml: float,
    ) -> bool:
        """Return True if the requested dose is valid."""

        if not self.enabled:
            return False

        return (
            self.minimum_dose_ml
            <= volume_ml
            <= self.maximum_dose_ml
        )

    def update_calibration(
        self,
        measured_ml: float,
        runtime_seconds: float,
    ) -> None:
        """Update the pump calibration."""

        if measured_ml <= 0:
            return

        if runtime_seconds <= 0:
            return

        self.ml_per_second = (
            measured_ml / runtime_seconds
        )

        self.calibration_factor = 1.0

        self.calibrated = True

    def to_dict(self) -> dict:
        """Serialize the pump."""

        return {
            "id": self.id,
            "name": self.name,
            "entity_id": self.entity_id,
            "ml_per_second": self.ml_per_second,
            "calibration_factor": self.calibration_factor,
            "calibrated": self.calibrated,
            "last_calibration": self.last_calibration,
            "minimum_dose_ml": self.minimum_dose_ml,
            "maximum_dose_ml": self.maximum_dose_ml,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> Pump:
        """Deserialize a pump."""

        return cls(
            id=data["id"],
            name=data["name"],
            entity_id=data.get("entity_id", ""),
            ml_per_second=data.get("ml_per_second", 1.0),
            calibration_factor=data.get("calibration_factor", 1.0),
            calibrated=data.get("calibrated", False),
            last_calibration=data.get("last_calibration"),
            minimum_dose_ml=data.get("minimum_dose_ml", 0.5),
            maximum_dose_ml=data.get("maximum_dose_ml", 100.0),
            enabled=data.get("enabled", True),
        )