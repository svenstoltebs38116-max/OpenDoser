"""Pump driver abstraction for OpenDoser."""

from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from .model.dosing_plan import DosingAction


class PumpDriver(ABC):
    """Abstract base class for pump drivers."""

    @abstractmethod
    async def execute_action(
        self,
        action: DosingAction,
    ) -> None:
        """Execute a dosing action."""