"""DataUpdateCoordinator for canvas_lms_integration."""

from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING, Any, List

from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import (
    CanvasLmsApiClient,
    CanvasLmsApiClientAuthenticationError,
    CanvasLmsApiClientError,
)
from .const import DOMAIN, LOGGER, CONF_OBSERVEE
from .data import CanvasLmsData

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from .data import CanvasLmsConfigEntry

# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class CanvasLmsDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: CanvasLmsConfigEntry

    def __init__(
            self,
            hass: HomeAssistant,
            client: CanvasLmsApiClient,
    ) -> None:
        """Initialize."""
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=1),
        )

        observee_id = self.config_entry.data[CONF_OBSERVEE]
        LOGGER.info("registering {}".format(observee_id))
        self.api = CanvasLmsData(hass, client, observee_id)
        self.available_entities: List[str] = []
        self.entities: List[Entity] = []

    async def _async_update_data(self) -> Any:
        """Update data via library."""
        data: dict[str, Any] = {}
        for entity in self.entities:
            if not entity.enabled:
                LOGGER.debug("Entity %s is disabled.", entity.entity_id)
                continue

            try:
                data[entity.entity_description.key] = await self.api.async_update(entity.entity_description.key)
            except CanvasLmsApiClientAuthenticationError as exception:
                raise ConfigEntryAuthFailed(exception) from exception
            except CanvasLmsApiClientError as exception:
                raise UpdateFailed(exception) from exception
            except Exception as exception:
                raise UpdateFailed(exception) from exception

        return data
