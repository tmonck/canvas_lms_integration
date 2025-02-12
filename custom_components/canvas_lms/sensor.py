"""Sensor platform for integration_blueprint."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN, LOGGER, Courses, MissingAssignments
from .coordinator import CanvasLmsDataUpdateCoordinator
from .entity import CanvasLmsEntity

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

    from .coordinator import CanvasLmsDataUpdateCoordinator
    from .data import CanvasLmsConfigEntry


@dataclass
class CanvasLmsEntityDescription(SensorEntityDescription):
    """Canvas LMS sensor entity description."""

    attributes_fn: Callable[[list[Any]], Mapping[str, Any] | None] = lambda _: None
    entity_registry_enabled_default: bool = False


ENTITY_DESCRIPTIONS = (
    CanvasLmsEntityDescription(
        key=MissingAssignments,
        name="Canvas LMS Missing Assignments",
        icon="mdi:format-quote-close",
        attributes_fn=lambda data: {"assignments": data, "count": len(data)},
    ),
    CanvasLmsEntityDescription(
        key=Courses,
        name="Canvas LMS Courses",
        icon="mdi:format-quote-close",
        attributes_fn=lambda data: {"courses": data, "count": len(data)},
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: CanvasLmsConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator: CanvasLmsDataUpdateCoordinator = hass.data[DOMAIN]
    entities = []
    for description in ENTITY_DESCRIPTIONS:
        entity = CanvasLmsSensor(coordinator, description, entry)
        coordinator.entities.append(entity)
        entities.append(entity)

    async_add_entities(entities, True)  # noqa: FBT003


class CanvasLmsSensor(CanvasLmsEntity, SensorEntity):
    """integration_blueprint Sensor class."""

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        entity_data = self.coordinator.data.get(self.entity_description.key, None)
        LOGGER.debug(
            f"retrieved entity_data {entity_data} for {self.entity_description}"
        )
        return len(entity_data) if entity_data else 0
