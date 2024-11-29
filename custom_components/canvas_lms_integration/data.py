"""Custom types for integration_blueprint."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .const import (
    MissingAssignments,
    Courses,
    LOGGER,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry

    from .api import CanvasLmsApiClient

type CanvasLmsConfigEntry = ConfigEntry[CanvasLmsData]


class CanvasLmsData:
    """Data for the CanvasLms integration."""

    def __init__(self, hass, client, observee_id):
        LOGGER.info("CanvasLmsData init with".format(observee_id))
        self.hass = hass
        self.client = client
        self.observee_id = observee_id
        self.entity_update_method = {
            Courses: self.async_update_classes,
            MissingAssignments: self.async_update_missing_assignments,
        }

    async def async_update(self, entity_key):
        """Update the data."""
        LOGGER.info("async_udpate called")
        if entity_key in self.entity_update_method:
            return await self.entity_update_method[entity_key]()

    async def async_update_missing_assignments(self):
        """Update obervees classes"""
        LOGGER.info("Retrieving missing assignments for {}".format(self.observee_id))
        return await self.client.async_get_missing_assignments(self.observee_id)

    async def async_update_classes(self):
        """Update obervees classes"""
        LOGGER.info("Retrieving courses for {}".format(self.observee_id))
        return await self.client.async_get_courses(self.observee_id)
