"""Wake SPCA connection."""

import logging

import aiohttp
from bs4 import BeautifulSoup

_LOGGER = logging.getLogger(__name__)


####################################################################################################

PETBRIDGE_URL_BASE = "https://petbridge.org/animals/animals-all-responsive.php"

ADOPTABLE_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog"
RECENTLY_ADOPTED_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog&Status=Adopted"


####################################################################################################


class WakeSpcaAnimal:
    """Wake SPCA Animal representation."""

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


class WakeSpcaClient:
    """Handle all data pulls from wakespca.org."""

    async def get_animals(self) -> list[WakeSpcaAnimal]:
        """Get the Animals from the current website data."""

        html_raw = await self._get_html(
            PETBRIDGE_URL_BASE + ADOPTABLE_DOGS_QUERY_PARAMS
        )

        html_parsed = BeautifulSoup(html_raw, "lxml")

        parsed_animals = []

        for entry in html_parsed.find_all("div", {"class": "animal_list_box"}):
            parsed_animals.append(WakeSpcaAnimal(entry))

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


# async def main():
#     """Main Entry Point."""

#     adoptable_animals = await WakeSpca.get_animals(ADOPTABLE_DOGS_QUERY_PARAMS)

#     for animal in adoptable_animals:

#         foster_care_pretty = ""
#         if animal.foster_care:
#             foster_care_pretty = "foster care"

#         adoption_pending_pretty = ""
#         if animal.adoption_pending:
#             adoption_pending_pretty = "adoption pending"

#         print("%-20s | %12s | %s" % (animal.name, foster_care_pretty, adoption_pending_pretty))

#     return


# if __name__ == "__main__":
#     s = time.perf_counter()
#     asyncio.run(main())
#     elapsed = time.perf_counter() - s
#     print(f"{__file__} executed in {elapsed:0.2f} seconds.")
