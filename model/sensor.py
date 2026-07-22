"""OpenDoser sensor model."""

from dataclasses import dataclass


@dataclass
class DoserSensor:
    """A configured Home Assistant sensor."""

    id: str
    entity_id: str
    name: str
    device_class: str