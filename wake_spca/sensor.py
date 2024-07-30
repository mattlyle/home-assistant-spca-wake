"""Sensor platform for Wake SPCA integration."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN, WAKE_SPCA_COORDINATOR
from .coordinator import WakeSpcaCoordinator
from .wake_spca import WakeSpcaAnimal

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