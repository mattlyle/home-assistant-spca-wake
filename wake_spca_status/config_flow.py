"""Config flow for the Vallox integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    CONF_ANIMAL_NAMES,
    CONF_REFRESH_INTERVAL,
    DEFAULT_REFRESH_INTERVAL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_ANIMAL_NAMES): cv.string,
        vol.Required(
            CONF_REFRESH_INTERVAL, default=DEFAULT_REFRESH_INTERVAL
        ): cv.positive_int,
    }
)


async def validate_refresh_interval(hass: HomeAssistant, refresh_interval: int) -> None:
    """Validate the refresh interval."""

    if refresh_interval < 15 or refresh_interval > 24 * 60:
        raise HomeAssistantError(f"Invalid refresh interval: {refresh_interval}")


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

        errors: dict[str, str] = {}

        animal_names = user_input[CONF_ANIMAL_NAMES]
        refresh_interval = user_input[CONF_REFRESH_INTERVAL]

        self._async_abort_entries_match(
            {CONF_ANIMAL_NAMES: animal_names, CONF_REFRESH_INTERVAL: refresh_interval}
        )

        try:
            await validate_refresh_interval(self.hass, refresh_interval)
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors[CONF_REFRESH_INTERVAL] = DEFAULT_REFRESH_INTERVAL
        else:
            return self.async_create_entry(
                title=DOMAIN,  # TODO is this correct?
                data={
                    **user_input,
                    CONF_ANIMAL_NAMES: "",
                    CONF_REFRESH_INTERVAL: DEFAULT_REFRESH_INTERVAL,
                },
            )

        return self.async_show_form(
            step_id="user",
            data_schema=self.add_suggested_values_to_schema(CONFIG_SCHEMA, user_input),
            errors=errors,
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
        updated_refresh_interval = user_input[CONF_REFRESH_INTERVAL]

        if (
            entry.data.get(CONF_ANIMAL_NAMES) != updated_animal_names
            or entry.data.get(CONF_REFRESH_INTERVAL) != updated_refresh_interval
        ):
            self._async_abort_entries_match(user_input)

        errors: dict[str, str] = {}

        try:
            await validate_refresh_interval(self.hass, updated_refresh_interval)
        except Exception:
            _LOGGER.exception("Unexpected exception")
            errors[CONF_REFRESH_INTERVAL] = DEFAULT_REFRESH_INTERVAL
        else:
            return self.async_update_reload_and_abort(
                entry,
                data={
                    **entry.data,
                    CONF_ANIMAL_NAMES: updated_animal_names,
                    CONF_REFRESH_INTERVAL: updated_refresh_interval,
                },
                reason="reconfigure_successful",
            )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=data_schema,
            errors=errors,
        )
