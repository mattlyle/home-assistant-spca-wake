"""Loading and parsing data from wakespca.org website."""

import logging

from bs4 import BeautifulSoup
import requests

_LOGGER = logging.getLogger(__name__)

PETBRIDGE_URL_BASE = "https://petbridge.org/animals/animals-all-responsive.php"

ADOPTABLE_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog"
RECENTLY_ADOPTED_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog&Status=Adopted"


class WakeSpcaAnimal:
    """Representation of an animal at WakeSPCA."""

    def __init__(self, bs4_entry) -> None:
        """Set up the model from the bs4 entry."""

        # self.id = animal_json["id"]
        # self.name = animal_json["name"]
        # self.status = animal_json["status"]
        # self.description = animal_json["description"]

        # self.raw = animal_json

        # dog name
        dog_name_node = bs4_entry.find("span", attrs={"class": "results_animal_name"})
        if not dog_name_node:
            raise InvalidConfigData("Dog name node not found")
        self.name = dog_name_node.text

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


class WakeSpca:
    """Util class to connect to and parse the wakespca.org website."""

    def _get_dogs_page(self, params) -> list[WakeSpcaAnimal]:
        """Get the dogs page and parses it."""

        html_raw = self.get_html(PETBRIDGE_URL_BASE + ADOPTABLE_DOGS_QUERY_PARAMS)

        html_parsed = BeautifulSoup(html_raw, "html5lib")

        # dogs = []
        # for entry in html_parsed.find_all("div", {"class": "animal_list_box"}):
        #     dogs.append(WakeSpcaAnimal(entry))
        # return dogs

        return [
            WakeSpcaAnimal(entry)
            for entry in html_parsed.find_all("div", {"class": "animal_list_box"})
        ]

    def _get_html(self, url):
        """Get the HTML for the specified URL."""

        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise InvalidConfigData(
                "Failed to fetch html: %d %s" % (response.status_code, response.reason)
            )

        return response.text

    def get_dogs(self) -> list[WakeSpcaAnimal]:
        """Get all the dogs on the page."""

        adoptable_dogs = self._get_dogs_page(ADOPTABLE_DOGS_QUERY_PARAMS)

        for dog in adoptable_dogs:
            foster_care = ""
            if dog.foster_care:
                foster_care = "foster care"

            adoption_pending = ""
            if dog.adoption_pending:
                adoption_pending = "adoption pending"

            s = "%-20s | %12s | %s" % (dog.name, foster_care, adoption_pending)
            _LOGGER.debug(s)

        return
