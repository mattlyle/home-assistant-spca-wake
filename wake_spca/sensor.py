"""Sensor platform for Wake SPCA integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, WAKE_SPCA_COORDINATOR
from .coordinator import WakeSpcaCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Wake SPCA Sensor Entities."""

    _LOGGER.info(">>> async_setup_entry")  # TODO remove

    coordinator: WakeSpcaCoordinator = hass.data[DOMAIN][entry.entry_id][
        WAKE_SPCA_COORDINATOR
    ]

    _LOGGER.info(f"Seeing {len(coordinator.animals)} animals")

    sensors = []
    for animal in coordinator.animals:
        _LOGGER.info(">>> Add")

    async_add_entities(sensors)
