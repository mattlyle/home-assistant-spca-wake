"""Constants for the Wake SPCA integration."""

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "wake_spca"
PLATFORMS = [
    Platform.SENSOR,
]

LOGGER: Final = logging.getLogger(__package__)

CONF_ANIMAL_NAMES: Final = "animal_names"
CONF_REFRESH_INTERVAL: Final = "refresh_interval"

DEFAULT_REFRESH_INTERVAL: Final = 60

DEFAULT_SCAN_INTERVAL: Final = 60

UPDATE_LISTENER: Final = "update_listener"
WAKE_SPCA_COORDINATOR: Final = "wake_spca_coordinator"