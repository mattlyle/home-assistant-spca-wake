"""Sensor platform for Wake SPCA integration."""

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, WAKE_SPCA_COORDINATOR, CONF_ANIMAL_NAMES
from .coordinator import WakeSpcaCoordinator
from .wake_spca import WakeSpcaAnimal

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set Up Wake SPCA Sensor Entities."""

    coordinator: WakeSpcaCoordinator = hass.data[DOMAIN][entry.entry_id][
        WAKE_SPCA_COORDINATOR
    ]

    target_animal_names_split = entry.data[CONF_ANIMAL_NAMES].split(",")

    sensors = []
    for animal_name in coordinator.animals.keys():
        for target_animal_name in target_animal_names_split:
            if animal_name.lower() == target_animal_name.strip().lower():
                sensors.append(
                    WakeSpcaAnimalAdoptionPendingSensor(coordinator, animal_name)
                )
                sensors.append(WakeSpcaAnimalInFosterSensor(coordinator, animal_name))

    async_add_entities(sensors)


class WakeSpcaAnimalAdoptionPendingSensor(CoordinatorEntity, SensorEntity):
    """Wake SPCA Animal Sensor for Adoption Pending."""

    def __init__(self, coordinator, animal_name) -> None:
        """Initialize the Sensor."""

        super().__init__(coordinator)
        self.animal_name = animal_name

    @property
    def animal_data(self) -> WakeSpcaAnimal:
        """Gets the animal data."""

        return self.coordinator.animals[self.animal_name]

    @property
    def device_data(self) -> dict[str, Any]:
        """Handle coordinator device data."""

        return self.coordinator.animals[self.animal_name].device

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""

        return DeviceInfo(
            {
                "identifiers": {(DOMAIN, self.animal_name)},
                "name": self.animal_name,
                "configuration_url": "https://www.spcawake.org",
                "manufacturer": "WakeSPCA",
                "model": "Dog",  # TODO should come from the data
            }
        )

    @property
    def unique_id(self) -> str:
        """Sets unique ID for this entity."""

        return str(self.animal_name) + "_adoption_pending"

        # TODO should fix spaces and characters

    @property
    def name(self) -> str:
        """Return name of the entity."""

        return "Adoption Pending"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""

        return True

    @property
    def icon(self) -> str:
        """Set icon for entity."""

        return "mdi:account-clock-outline"

    @property
    def native_value(self) -> str:
        """Return if an adoption is pending."""

        if self.coordinator.animals[self.animal_name].adoption_pending:
            return "Yes"

        return "No"

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return entity device class."""
        return SensorDeviceClass.ENUM

    @property
    def entity_category(self) -> EntityCategory:
        """Set category to diagnostic."""
        return EntityCategory.DIAGNOSTIC


class WakeSpcaAnimalInFosterSensor(CoordinatorEntity, SensorEntity):
    """Wake SPCA Animal Sensor for In Foster Care."""

    def __init__(self, coordinator, animal_name) -> None:
        """Initialize the Sensor."""

        super().__init__(coordinator)
        self.animal_name = animal_name

    @property
    def animal_data(self) -> WakeSpcaAnimal:
        """Gets the animal data."""

        return self.coordinator.animals[self.animal_name]

    @property
    def device_data(self) -> dict[str, Any]:
        """Handle coordinator device data."""

        return self.coordinator.animals[self.animal_name].device

    @property
    def device_info(self) -> DeviceInfo:
        """Return device registry information for this entity."""

        return DeviceInfo(
            {
                "identifiers": {(DOMAIN, self.animal_name)},
                "name": self.animal_name,
                "configuration_url": "https://www.spcawake.org",
                "manufacturer": "WakeSPCA",
                "model": "Dog",  # TODO should come from the data
            }
        )

    @property
    def unique_id(self) -> str:
        """Sets unique ID for this entity."""

        return str(self.animal_name) + "_in_foster_care"

        # TODO should fix spaces and characters

    @property
    def name(self) -> str:
        """Return name of the entity."""

        return "In Foster Care"

    @property
    def has_entity_name(self) -> bool:
        """Indicate that entity has name defined."""

        return True

    @property
    def icon(self) -> str:
        """Set icon for entity."""

        return "mdi:home"

    @property
    def native_value(self) -> str:
        """Return if the animal is in foster care."""

        if self.coordinator.animals[self.animal_name].foster_care:
            return "Yes"

        return "No"

    @property
    def device_class(self) -> SensorDeviceClass:
        """Return entity device class."""
        return SensorDeviceClass.ENUM

    @property
    def entity_category(self) -> EntityCategory:
        """Set category to diagnostic."""
        return EntityCategory.DIAGNOSTIC


class WakeSpcaAnimalAdoptedSensor(CoordinatorEntity, SensorEntity):
    """Wake SPCA Animal Sensor for Adopted."""
