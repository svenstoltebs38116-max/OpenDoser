"""OpenDoser role definitions."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class RoleDefinition:
    """Definition of a logical OpenDoser role."""

    label: str
    domain: str
    optional: bool = False


class Role(str, Enum):
    """Logical OpenDoser roles."""

    # Sensors
    PH_SENSOR = "ph_sensor"
    EC_SENSOR = "ec_sensor"
    TEMPERATURE_SENSOR = "temperature_sensor"
    LEVEL_SENSOR = "level_sensor"

    # Pumps
    PH_UP_PUMP = "ph_up_pump"
    PH_DOWN_PUMP = "ph_down_pump"

    EC_A_PUMP = "ec_a_pump"
    EC_B_PUMP = "ec_b_pump"

    # Outputs
    MIXER = "mixer"
    FILL_VALVE = "fill_valve"
    DRAIN_VALVE = "drain_valve"
    CIRCULATION_PUMP = "circulation_pump"


ROLE_DEFINITIONS: dict[Role, RoleDefinition] = {
    # Sensors
    Role.PH_SENSOR: RoleDefinition(
        label="pH Sensor",
        domain="sensor",
    ),
    Role.EC_SENSOR: RoleDefinition(
        label="EC Sensor",
        domain="sensor",
    ),
    Role.TEMPERATURE_SENSOR: RoleDefinition(
        label="Temperature Sensor",
        domain="sensor",
    ),
    Role.LEVEL_SENSOR: RoleDefinition(
        label="Level Sensor",
        domain="sensor",
        optional=True,
    ),

    # Pumps
    Role.PH_UP_PUMP: RoleDefinition(
        label="pH Up Pump",
        domain="switch",
        optional=True,
    ),
    Role.PH_DOWN_PUMP: RoleDefinition(
        label="pH Down Pump",
        domain="switch",
        optional=True,
    ),
    Role.EC_A_PUMP: RoleDefinition(
        label="EC A Pump",
        domain="switch",
        optional=True,
    ),
    Role.EC_B_PUMP: RoleDefinition(
        label="EC B Pump",
        domain="switch",
        optional=True,
    ),

    # Outputs
    Role.MIXER: RoleDefinition(
        label="Mixer",
        domain="switch",
        optional=True,
    ),
    Role.FILL_VALVE: RoleDefinition(
        label="Fill Valve",
        domain="switch",
        optional=True,
    ),
    Role.DRAIN_VALVE: RoleDefinition(
        label="Drain Valve",
        domain="switch",
        optional=True,
    ),
    Role.CIRCULATION_PUMP: RoleDefinition(
        label="Circulation Pump",
        domain="switch",
        optional=True,
    ),
}