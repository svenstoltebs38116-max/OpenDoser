"""Pump calibration."""

from __future__ import annotations

from .model.pump import Pump


class PumpCalibration:
    """Handles pump calibration."""

    @staticmethod
    def calibrate(
        pump: Pump,
        measured_ml: float,
        runtime_seconds: float,
    ) -> None:
        """Calibrate a pump."""

        if measured_ml <= 0:
            raise ValueError("Measured volume must be greater than zero.")

        if runtime_seconds <= 0:
            raise ValueError("Runtime must be greater than zero.")

        pump.update_calibration(
            measured_ml,
            runtime_seconds,
        )