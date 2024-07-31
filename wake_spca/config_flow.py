"""Config flow for the Vallox integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers import config_validation as cv

from .const import CONF_ANIMAL_NAMES, DOMAIN

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ANIMAL_NAMES): cv.string,
    }
)


class WakeSpcaConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for the Wake SPCA integration."""

    VERSION = 1

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

        self._async_abort_entries_match({CONF_ANIMAL_NAMES: animal_names})

        return self.async_create_entry(
            title=DOMAIN,
            data={**user_input, CONF_ANIMAL_NAMES: ""},
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle reconfiguration of the Wake SPCA config."""

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

        if entry.data.get(CONF_ANIMAL_NAMES) != updated_animal_names:
            self._async_abort_entries_match(user_input)

        return self.async_update_reload_and_abort(
            entry,
            data={
                **entry.data,
                CONF_ANIMAL_NAMES: updated_animal_names,
            },
            reason="reconfigure_successful",
        )
