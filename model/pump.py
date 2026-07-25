"""OpenDoser pump model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from ..roles import Role


@dataclass(slots=True)
class Pump:
    """Represents a dosing pump."""

    #
    # Identity
    #

    id: str
    name: str
    role: Role

    #
    # Driver
    #

    driver: dict[str, Any] = field(
        default_factory=lambda: {
            "type": "entity",
            "entity_id": "",
        },
    )

    #
    # Calibration
    #

    ml_per_second: float = 1.0

    calibration_factor: float = 1.0

    calibrated: bool = False

    last_calibration: str | None = None

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
            "role": self.role.value,
            "driver": self.driver,
            "ml_per_second": self.ml_per_second,
            "calibration_factor": self.calibration_factor,
            "calibrated": self.calibrated,
            "last_calibration": self.last_calibration,
            "enabled": self.enabled,
        }

    @classmethod
    def from_dict(
        cls,
        data: dict,
    ) -> Pump:
        """Deserialize a pump."""

        if "driver" in data:
            driver = data["driver"]
        else:
            driver = {
                "type": "entity",
                "entity_id": data.get("entity_id", ""),
            }

        #
        # Migration for older configurations
        #

        role_name = data.get("role")

        if role_name is None:
            pump_id = data.get("id", "")

            mapping = {
                "pump_ph_down": Role.PH_DOWN_PUMP,
                "pump_ph_up": Role.PH_UP_PUMP,
                "pump_ec": Role.EC_A_PUMP,
                "ec_a": Role.EC_A_PUMP,
                "ec_b": Role.EC_B_PUMP,
            }

            role = mapping.get(
                pump_id,
                Role.EC_A_PUMP,
            )
        else:
            role = Role(role_name)

        return cls(
            id=data["id"],
            name=data["name"],
            role=role,
            driver=driver,
            ml_per_second=data.get("ml_per_second", 1.0),
            calibration_factor=data.get("calibration_factor", 1.0),
            calibrated=data.get("calibrated", False),
            last_calibration=data.get("last_calibration"),
            enabled=data.get("enabled", True),
        )