"""CanvasLmsEntity class."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.json import ExtendedJSONEncoder
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import ATTRIBUTION, DOMAIN, LOGGER, NAME, VERSION
from .coordinator import CanvasLmsDataUpdateCoordinator

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .data import CanvasLmsConfigEntry, CanvasLmsEntityDescription

class CanvasLmsEntity(CoordinatorEntity[CanvasLmsDataUpdateCoordinator]):
    """CanvasLmsEntity class."""

    _attr_attribution = ATTRIBUTION

    def __init__(
            self,
            coordinator: CanvasLmsDataUpdateCoordinator,
            description: CanvasLmsEntityDescription,
            config_entry: CanvasLmsConfigEntry) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._attr_name = f"{config_entry.title} {description.name}"
        self._attr_unique_id = f"{config_entry.entry_id}{description.key.lower()}"
        LOGGER.debug(f"creating entity with _attr_unique_id of {self._attr_unique_id}")
        self._attr_device_info = DeviceInfo(
            identifiers={
                (
                    DOMAIN,
                    # observee_id,
                    coordinator.config_entry.entry_id,
                ),
            },
        )
        self.entity_description = description

    @property
    def device_info(self) -> DeviceInfo:
        """Grocy device information."""
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.config_entry.entry_id)},
            name=NAME,
            manufacturer=NAME,
            sw_version=VERSION,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def extra_state_attributes(self) -> Mapping[str, Any] | None:
        """Return the extra state attributes."""
        data = self.coordinator.data.get(self.entity_description.key)
        if data and hasattr(self.entity_description, "attributes_fn"):
            return json.loads(
                json.dumps(
                    self.entity_description.attributes_fn(data),
                    cls=ExtendedJSONEncoder,
                )
            )

        return None
