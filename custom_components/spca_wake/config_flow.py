"""Config flow for the Vallox integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_ANIMAL_NAMES,
    CONF_PETFINDER_API_KEY,
    CONF_PETFINDER_SECRET,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ANIMAL_NAMES): cv.string,
        vol.Required(CONF_PETFINDER_API_KEY): cv.string,
        vol.Required(CONF_PETFINDER_SECRET): cv.string,
    }
)


class SpcaWakeConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the SPCA Wake integration."""

    VERSION = 2

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=CONFIG_SCHEMA,
            )

        animal_names = user_input[CONF_ANIMAL_NAMES]
        petfinder_api_key = user_input[CONF_PETFINDER_API_KEY]
        petfinder_secret = user_input[CONF_PETFINDER_SECRET]

        self._async_abort_entries_match(
            {
                CONF_ANIMAL_NAMES: animal_names,
                CONF_PETFINDER_API_KEY: petfinder_api_key,
                CONF_PETFINDER_SECRET: petfinder_secret,
            }
        )

        return self.async_create_entry(
            title=DOMAIN,
            data={
                **user_input,
                CONF_ANIMAL_NAMES: animal_names,
                CONF_PETFINDER_API_KEY: petfinder_api_key,
                CONF_PETFINDER_SECRET: petfinder_secret,
            },
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the SPCA Wake config."""

        entry = self.hass.config_entries.async_get_entry(self.context["entry_id"])
        assert entry

        data_schema = self.add_suggested_values_to_schema(CONFIG_SCHEMA, entry.data)
        if user_input:
            data_schema = self.add_suggested_values_to_schema(data_schema, user_input)

        if not user_input:
            return self.async_show_form(
                step_id="reconfigure",
                data_schema=data_schema,
            )

        updated_animal_names = user_input[CONF_ANIMAL_NAMES]
        updated_petfinder_api_key = user_input[CONF_PETFINDER_API_KEY]
        updated_petfinder_secret = user_input[CONF_PETFINDER_SECRET]

        self._async_abort_entries_match(
            {
                CONF_ANIMAL_NAMES: updated_animal_names,
                CONF_PETFINDER_API_KEY: updated_petfinder_api_key,
                CONF_PETFINDER_SECRET: updated_petfinder_secret,
            }
        )

        return self.async_update_reload_and_abort(
            entry,
            data={
                **entry.data,
                CONF_ANIMAL_NAMES: updated_animal_names,
                CONF_PETFINDER_API_KEY: updated_petfinder_api_key,
                CONF_PETFINDER_SECRET: updated_petfinder_secret,
            },
            reason="reconfigure_successful",
        )
