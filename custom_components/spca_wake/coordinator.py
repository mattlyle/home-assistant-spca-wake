"""SPCA Wake Coordinator."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN
from .spca_wake_web import SpcaWakeAnimal, SpcaWakeClient

_LOGGER = logging.getLogger(__name__)


class SpcaWakeCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    animals: dict[str, SpcaWakeAnimal] = {}

    def __init__(self, hass: HomeAssistant, my_api: Any) -> None:
        """Initialize the coordinator."""

        self.my_api = my_api
        self.client = SpcaWakeClient()

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=60 * 15),
            always_update=True,
        )

    async def _async_update_data(self) -> list[SpcaWakeAnimal]:
        """Fetch data from SPCA Wake Website."""

        _LOGGER.warning("Fetching animals from spcawake.org")  # TODO remove

        try:
            animals = await self.client.get_animals()
        except Exception as error:
            raise UpdateFailed(error) from error

        if len(animals) == 0:
            raise UpdateFailed("No animals found")

        self.animals = {}
        for animal in animals:
            self.animals[animal.name] = animal

        return animals
