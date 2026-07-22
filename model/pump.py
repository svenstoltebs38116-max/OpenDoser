"""OpenDoser pump model."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Pump:
    """Represents a dosing pump."""

    id: str
    name: str

    #
    # Calibration
    #

    ml_per_second: float = 1.0

    calibration_factor: float = 1.0

    #
    # Limits
    #

    minimum_dose_ml: float = 0.5

    maximum_dose_ml: float = 100.0

    enabled: bool = True

    def effective_flow_rate(self) -> float:
        """Return the calibrated flow rate."""

        return self.ml_per_second * self.calibration_factor

    def runtime_for(self, volume_ml: float) -> float:
        """Return the runtime in seconds."""

        flow = self.effective_flow_rate()

        if flow <= 0:
            return 0.0

        return volume_ml / flow

    def can_dose(self, volume_ml: float) -> bool:
        """Return True if the requested dose is valid."""

        return (
            self.enabled
            and self.minimum_dose_ml <= volume_ml <= self.maximum_dose_ml
        )