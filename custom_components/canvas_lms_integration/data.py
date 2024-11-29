"""Custom types for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from .const import (
    LOGGER,
    Courses,
    MissingAssignments,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .const import CanvasLmsApiClient

type CanvasLmsConfigEntry = ConfigEntry[CanvasLmsData]


class CanvasLmsData:
    """Data for the CanvasLms integration."""

    def __init__(
            self,
            hass: HomeAssistant,
            client: CanvasLmsApiClient,
            observee_id: str
    ):
        """Initialize Canvas LMS Data."""
        LOGGER.debug(f"CanvasLmsData init with {observee_id}")
        self.hass = hass
        self.client = client
        self.observee_id = observee_id
        self.entity_update_method = {
            Courses: self.async_update_classes,
            MissingAssignments: self.async_update_missing_assignments,
        }

    async def async_update(self, entity_key: str) -> Any:
        """Update the data."""
        if entity_key in self.entity_update_method:
            return await self.entity_update_method[entity_key]()

        return None

    async def async_update_missing_assignments(self) -> Any:
        """Update obervees classes."""
        LOGGER.debug(f"Retrieving missing assignments for {self.observee_id}")
        return await self.client.async_get_missing_assignments(self.observee_id)

    async def async_update_classes(self) -> Any:
        """Update obervees classes."""
        LOGGER.debug(f"Retrieving courses for {self.observee_id}")
        return await self.client.async_get_courses(self.observee_id)
