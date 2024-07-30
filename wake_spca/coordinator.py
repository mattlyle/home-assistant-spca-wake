"""Wake SPCA Coordinator."""

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DEFAULT_SCAN_INTERVAL, DOMAIN
from .wake_spca import WakeSpcaAnimal, WakeSpcaClient

_LOGGER = logging.getLogger(__name__)


class WakeSpcaCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    animals: list[WakeSpcaAnimal] = []

    def __init__(self, hass: HomeAssistant, my_api: Any) -> None:
        """Initialize the coordinator."""

        self.my_api = my_api
        self.client = WakeSpcaClient()

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
            always_update=True,
        )

    async def _async_update_data(self) -> list[WakeSpcaAnimal]:
        """Fetch data from Wake SPCA Website."""

        _LOGGER.info("Fetching animals from wakespca.org")  # TODO remove

        try:
            animals = await self.client.get_animals()
        except Exception as error:
            raise UpdateFailed(error) from error

        if len(animals) == 0:
            raise UpdateFailed("No animals found")

        return animals
