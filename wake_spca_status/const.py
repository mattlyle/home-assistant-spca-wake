"""Constants for the Wake SPCA Status integration."""

import logging
from typing import Final

DOMAIN: Final = "wake_spca_status"
LOGGER: Final = logging.getLogger(__package__)

CONF_ANIMAL_NAMES: Final = "animal_names"
CONF_SCAN_INTERVAL: Final = "scan_interval"

DEFAULT_SCAN_INTERVAL: Final = 60  # in minutes
