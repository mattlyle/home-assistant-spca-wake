"""SPCA Wake connection."""

import json
import logging
from urllib.parse import parse_qs, urlparse

import aiohttp
from bs4 import BeautifulSoup

from homeassistant.exceptions import HomeAssistantError

_LOGGER = logging.getLogger(__name__)


####################################################################################################

PETBRIDGE_URL_BASE = "https://petbridge.org/animals/animals-all-responsive.php"
PETBRIDGE_ADOPTABLE_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog"
PETBRIDGE_RECENTLY_ADOPTED_DOGS_QUERY_PARAMS = "?ClientID=24&Species=Dog&Status=Adopted"

PETFINDER_API_URL_BASE = "https://api.petfinder.com"
PETFINDER_API_QUERY_PARAMS = "/v2/animals?type=dog&limit=100&organization=NC590"
# PETFINDER_API_QUERY_PARAMS = "/v2/animals?type=dog&location=27603&distance=25&limit=100"

####################################################################################################


class SpcaWakeAnimal:
    """SPCA Wake Animal representation."""

    id: str = ""

    name: str = ""

    foster_care: bool = False

    adoption_pending: bool = False

    on_sleepover: bool = False

    is_adopted: bool = False

    # breeds
    # url
    # environment
    #   children
    #   dogs
    #   cats
    # tags

    def __init__(self) -> None:
        """Construct the instance."""


class SpcaWakeClient:
    """Handle all data pulls from spcawake.org."""

    def __init__(self, petfinder_api_key: str, petfinder_api_secret: str) -> None:
        """Initialize the client."""

        self.petfinder_api_key = petfinder_api_key
        self.petfinder_api_secret = petfinder_api_secret

    async def get_animals(
        self,
    ) -> list[SpcaWakeAnimal]:
        """Get the animals."""

        animals: list[SpcaWakeAnimal] = []

        # get from petfinder
        petfinder_animal_lookup: dict[str, SpcaWakeAnimal] = {}
        petfinder_animals = await self._get_from_petfinder()
        for petfinder_animal in petfinder_animals:
            petfinder_animal_lookup[petfinder_animal.id] = petfinder_animal

        website_animal_lookup: dict[str, SpcaWakeAnimal] = {}

        # add the adoptable dogs
        adoptable_animals = await self._get_from_petbridge(
            PETBRIDGE_ADOPTABLE_DOGS_QUERY_PARAMS
        )
        for spcawake_animal in adoptable_animals:
            animals.append(spcawake_animal)
            website_animal_lookup[spcawake_animal.id] = spcawake_animal

        # add the recently adopted dogs
        recently_adopted_animals = await self._get_from_petbridge(
            PETBRIDGE_RECENTLY_ADOPTED_DOGS_QUERY_PARAMS
        )
        for spcawake_animal in recently_adopted_animals:
            animals.append(spcawake_animal)
            website_animal_lookup[spcawake_animal.id] = spcawake_animal

        # now find animals that are in petfinder, but not the website
        for petfinder_animal in petfinder_animals:
            if petfinder_animal.id not in website_animal_lookup:
                petfinder_animal.on_sleepover = True
                animals.append(petfinder_animal)

        return animals

    def _animal_from_petbridge_html(self, bs4_node) -> SpcaWakeAnimal:
        animal: SpcaWakeAnimal = SpcaWakeAnimal()

        # name
        animal_name_node = bs4_node.find("span", attrs={"class": "results_animal_name"})
        if not animal_name_node:
            raise HomeAssistantError("Animal name node not found")
        animal.name = animal_name_node.text

        # foster care
        location_node = bs4_node.find(
            "div", attrs={"class": "results_animals_location"}
        )
        animal.foster_care = location_node and "foster" in location_node.text

        # adoption pending and is adopted
        adoption_pending_node = bs4_node.find(
            "div", attrs={"class": "results_animals_status"}
        )
        animal.adoption_pending = (
            adoption_pending_node and "adoption pending" in adoption_pending_node.text
        )
        animal.is_adopted = (
            adoption_pending_node
            and "already been adopted" in adoption_pending_node.text
        )

        # animal id
        details_node = bs4_node.find("a", attrs={"class": "results_animal_link"})
        if not hasattr(details_node, "href"):
            raise HomeAssistantError("Animal link not found")
        parsed_query_string = parse_qs(urlparse(details_node["href"]).query)
        animal.id = "A%06d" % int(parsed_query_string["aid"][0])

        return animal

    async def _get_from_petbridge(self, request_params: str) -> list[SpcaWakeAnimal]:
        """Fetch and parses a page of animal results."""

        html_raw = await self._run_http_get(PETBRIDGE_URL_BASE + request_params, None)
        html_parsed = BeautifulSoup(html_raw, "lxml")

        parsed_animals = []

        for entry in html_parsed.find_all("div", {"class": "animal_list_box"}):
            parsed_animals.append(self._animal_from_petbridge_html(entry))  # noqa: PERF401

        return parsed_animals

    async def _get_from_petfinder(self) -> list[SpcaWakeAnimal]:
        token = await self._get_petfinder_new_token(
            self.petfinder_api_key, self.petfinder_api_secret
        )

        return await self._petfinder_api_call(PETFINDER_API_QUERY_PARAMS, token)

    def _animal_from_petfinder_json(self, json_node) -> SpcaWakeAnimal:
        animal: SpcaWakeAnimal = SpcaWakeAnimal()
        animal.id = json_node["organization_animal_id"]
        animal.name = json_node["name"].capitalize()

        # animal.type = json_node["type"]
        # animal.status = json_node["status"]
        # animal.altId = json_node["id"]

        return animal

    async def _petfinder_api_call(
        self, request_params: str, token: str
    ) -> list[SpcaWakeAnimal]:
        parsed_animals: list[SpcaWakeAnimal] = []

        keep_going = True
        while keep_going:
            raw_json_response = await self._run_http_get(
                PETFINDER_API_URL_BASE + request_params,
                {"Authorization": "Bearer " + token},
            )
            animals_response = json.loads(raw_json_response)

            for petfinder_animal in animals_response["animals"]:
                parsed_animals.append(  # noqa: PERF401
                    self._animal_from_petfinder_json(petfinder_animal)
                )

            keep_going = False

            if "pagination" not in animals_response:
                raise HomeAssistantError("Pagination not in response!")

            if (
                "_links" in animals_response["pagination"]
                and "next" in animals_response["pagination"]["_links"]
                and "href" in animals_response["pagination"]["_links"]["next"]
            ):
                request_params = animals_response["pagination"]["_links"]["next"][
                    "href"
                ]
                keep_going = True

        return parsed_animals

    async def _get_petfinder_new_token(self, api_key, api_secret):
        response_json_raw = await self._run_http_post(
            PETFINDER_API_URL_BASE + "/v2/oauth2/token",
            {
                "grant_type": "client_credentials",
                "client_id": api_key,
                "client_secret": api_secret,
            },
        )

        return json.loads(response_json_raw)["access_token"]

    async def _run_http_get(self, url: str, extra_headers: dict[str, str]) -> str:
        """Get the HTML from the given URL."""

        headers = {"Connection": "close"}
        if extra_headers:
            for key, value in extra_headers.items():
                headers[key] = value  # noqa: PERF403

        async with (
            aiohttp.ClientSession() as session,
            session.get(url, headers=headers) as response,
        ):
            if response.status != 200:
                raise HomeAssistantError(
                    "Failed to fetch html: %d %s"
                    % (response.status_code, response.reason)
                )
            return await response.text()

    async def _run_http_post(self, url: str, data: dict[str:str]) -> str:
        """Get the HTML from the given URL."""

        async with (
            aiohttp.ClientSession() as session,
            session.post(
                url=url, data=data, headers=[("Connection", "close")]
            ) as response,
        ):
            if response.status != 200:
                raise HomeAssistantError(
                    "Failed to fetch html: %d %s"
                    % (response.status_code, response.reason)
                )
            return await response.text()
