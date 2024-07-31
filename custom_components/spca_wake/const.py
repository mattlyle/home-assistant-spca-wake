"""Constants for the SPCA Wake integration."""

import logging
from typing import Final

from homeassistant.const import Platform

DOMAIN: Final = "spca_wake"
PLATFORMS = [
    Platform.SENSOR,
]

LOGGER: Final = logging.getLogger(__package__)

CONF_ANIMAL_NAMES: Final = "animal_names"
CONF_SENSOR_ATTRIBUTION: Final = "Data from spcawake.org"

UPDATE_LISTENER: Final = "update_listener"
SPCA_WAKE_COORDINATOR: Final = "spca_wake_coordinator"
