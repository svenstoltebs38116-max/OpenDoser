"""Persistent storage for OpenDoser."""

from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers.storage import Store

from .configuration import Configuration
from .const import DOMAIN
from .model.system import System

_STORAGE_VERSION = 1
_STORAGE_KEY = f"{DOMAIN}.system"


class SystemStorage:
    """Stores and loads the OpenDoser configuration."""

    def __init__(
        self,
        hass: HomeAssistant,
    ) -> None:
        """Initialize storage."""

        self._store: Store = Store(
            hass,
            _STORAGE_VERSION,
            _STORAGE_KEY,
        )

    async def load(self) -> System:
        """Load the current system."""

        data = await self._store.async_load()

        if data is None:
            system = Configuration.create_default_system()
            await self.save(system)
            return system

        return System.from_dict(data)

    async def save(
        self,
        system: System,
    ) -> None:
        """Save the current system."""

        await self._store.async_save(
            system.to_dict(),
        )