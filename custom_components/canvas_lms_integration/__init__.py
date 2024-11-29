"""
Custom integration to integrate integration_blueprint with Home Assistant.

For more details about this integration, please refer to
https://github.com/ludeeus/integration_blueprint
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from homeassistant.const import CONF_ACCESS_TOKEN, Platform
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import CanvasLmsApiClient
from .const import CONF_CANVAS_URL, DOMAIN
from .coordinator import CanvasLmsDataUpdateCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import CanvasLmsConfigEntry

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
]


# https://developers.home-assistant.io/docs/config_entries_index/#setting-up-an-entry
async def async_setup_entry(
    hass: HomeAssistant,
    entry: CanvasLmsConfigEntry,
) -> bool:
    """Set up this integration using UI."""
    client = CanvasLmsApiClient(
        canvas_base_url=entry.data[CONF_CANVAS_URL],
        apiKey=entry.data[CONF_ACCESS_TOKEN],
        session=async_get_clientsession(hass)
    )
    coordinator = CanvasLmsDataUpdateCoordinator(
        hass=hass,
        client=client,
    )

    # https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
    await coordinator.async_config_entry_first_refresh()
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: CanvasLmsConfigEntry,
) -> bool:
    """Handle removal of an entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(
    hass: HomeAssistant,
    entry: CanvasLmsConfigEntry,
) -> None:
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
