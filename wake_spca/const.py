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
CONF_SENSOR_ATTRIBUTION: Final = "Data from spcawake.org"

UPDATE_LISTENER: Final = "update_listener"
WAKE_SPCA_COORDINATOR: Final = "wake_spca_coordinator"
