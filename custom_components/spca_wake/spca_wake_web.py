"""SPCA Wake connection."""

import logging

import aiohttp
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)


####################################################################################################

PETBRIDGE_URL_BASE = "https://petbridge.org/animals/animals-all-responsive.php"

ADOPTABLE_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog"
RECENTLY_ADOPTED_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog&Status=Adopted"


####################################################################################################


class SpcaWakeAnimal:
    """SPCA Wake Animal representation."""

    def __init__(self, bs4_entry) -> None:
        """Construct the instance."""

        # name
        animal_name_node = bs4_entry.find(
            "span", attrs={"class": "results_animal_name"}
        )
        if not animal_name_node:
            raise Exception("Animal name node not found")
        self.name = animal_name_node.text

        # foster care
        location_node = bs4_entry.find(
            "div", attrs={"class": "results_animals_location"}
        )
        self.foster_care = location_node and "foster" in location_node.text

        # adoption pending
        adoption_pending_node = bs4_entry.find(
            "div", attrs={"class": "results_animals_status"}
        )
        self.adoption_pending = (
            adoption_pending_node and "adoption pending" in adoption_pending_node.text
        )
        self.is_adopted = (
            adoption_pending_node
            and "already been adopted" in adoption_pending_node.text
        )


class SpcaWakeClient:
    """Handle all data pulls from spcawake.org."""

    async def get_animals(self) -> list[SpcaWakeAnimal]:
        """Get the Animals from the current website data."""

        animals: list[SpcaWakeAnimal] = []

        # add the available dogs
        animals.extend(
            await self._parse_page(PETBRIDGE_URL_BASE + ADOPTABLE_DOGS_QUERY_PARAMS)
        )

        # add the recently adopted dogs
        animals.extend(
            await self._parse_page(
                PETBRIDGE_URL_BASE + RECENTLY_ADOPTED_DOGS_QUERY_PARAMS
            )
        )

        return animals

    async def _parse_page(self, url: str) -> list[SpcaWakeAnimal]:
        """Fetch and parses a page of animal results."""

        html_raw = await self._get_html(url)
        html_parsed = BeautifulSoup(html_raw, "lxml")

        parsed_animals = []

        for entry in html_parsed.find_all("div", {"class": "animal_list_box"}):
            parsed_animals.append(SpcaWakeAnimal(entry))

        return parsed_animals

    async def _get_html(self, url: str) -> str:
        """Get the HTML from the given URL."""

        # response = requests.get(url)
        # if response.status_code != 200:
        #     raise Exception(
        #         "Failed to fetch html: %d %s" % (response.status_code, response.reason)
        #     )
        # return response.text

        _LOGGER.info(url)
        async with aiohttp.ClientSession() as session, session.get(url) as response:
            if response.status != 200:
                raise Exception(
                    "Failed to fetch html: %d %s"
                    % (response.status_code, response.reason)
                )
            return await response.text()


####################################################################################################
