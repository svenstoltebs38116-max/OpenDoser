"""OpenDoser panel registration."""

from __future__ import annotations

from homeassistant.components import panel_custom
from homeassistant.core import HomeAssistant

from .const import DOMAIN


async def async_setup_panel(
    hass: HomeAssistant,
) -> None:
    """Register the OpenDoser panel."""

    await panel_custom.async_register_panel(
        hass,
        frontend_url_path=DOMAIN,
        webcomponent_name="opendoser-panel",
        module_url=f"/{DOMAIN}/frontend/opendoser-panel.js",
        sidebar_title="OpenDoser",
        sidebar_icon="mdi:flask",
        require_admin=True,
        config={
            "_panel_custom": {
                "name": "opendoser-panel",
            },
        },
    )