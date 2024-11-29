"""Adds config flow for Canvas LMS."""

from __future__ import annotations

import logging
from typing import Any, Dict

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from canvasapi.exceptions import InvalidAccessToken
from homeassistant import config_entries, data_entry_flow
from homeassistant.const import CONF_ACCESS_TOKEN
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    CanvasLmsApiClient,
    CanvasLmsApiClientAuthenticationError,
    CanvasLmsApiClientCommunicationError,
    CanvasLmsApiClientError,
)
from .const import (
    CONF_CANVAS_URL,
    # CONF_COURSES,
    CONF_OBSERVEE,
    CONF_OBSERVEES,
    DOMAIN,
    LOGGER,
)

_LOGGER = logging.getLogger(__name__)

observees = {}
usernames = []


class CanvasLmsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Canvas LMS."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> data_entry_flow.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    canvas_url=user_input[CONF_CANVAS_URL],
                    password=user_input[CONF_ACCESS_TOKEN],
                )
            except CanvasLmsApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except CanvasLmsApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except CanvasLmsApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                await self._retrieve_available_observees(
                    canvas_url=user_input[CONF_CANVAS_URL],
                    token=user_input[CONF_ACCESS_TOKEN],
                )
                self.data = {
                    CONF_CANVAS_URL: user_input[CONF_CANVAS_URL],
                    CONF_ACCESS_TOKEN: user_input[CONF_ACCESS_TOKEN]
                }
                return await self.async_step_observees()

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_CANVAS_URL,
                        default=(user_input or {}).get(CONF_CANVAS_URL, vol.UNDEFINED),
                    ): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.TEXT,
                        ),
                    ),
                    vol.Required(CONF_ACCESS_TOKEN): selector.TextSelector(
                        selector.TextSelectorConfig(
                            type=selector.TextSelectorType.PASSWORD,
                        ),
                    ),
                },
            ),
            errors=_errors,
        )

    async def async_step_observees(
        self, user_input: Dict[str, Any] | Any = None
    ) -> data_entry_flow.FlowResult:
        """Something."""
        observee_schema = vol.Schema(
            {
                vol.Required(CONF_OBSERVEE): selector.SelectSelector(
                    selector.SelectSelectorConfig(
                        options=usernames,
                        multiple=False,
                        mode=selector.SelectSelectorMode.DROPDOWN,
                    )
                )
            }
        )

        errors: dict[str, str] = {}
        if user_input is not None:
            observee = user_input.get(CONF_OBSERVEE)
            self.data[CONF_OBSERVEE] = observee # The value that is selected is already the id
            return self.async_create_entry(
                title=observees[int(observee)]["name"],
                data=self.data
            )

        return self.async_show_form(
            step_id="observees", data_schema=observee_schema, errors=errors
        )

    async def _test_credentials(self, canvas_url: str, password: str) -> None:
        """Validate credentials."""
        client = CanvasLmsApiClient(
            canvas_base_url=canvas_url,
            apiKey=password,
            session=async_create_clientsession(self.hass),
        )
        self._canvas = client
        await client.async_get_user("self")

    async def _retrieve_available_observees(self, canvas_url: str, token: str) -> None:
        try:
            _observees = await self._canvas.async_get_observees("self")
            for observee in _observees:
                observees[observee["id"]] = observee
                usernames.append({"value": str(observee["id"]), "label": observee["name"]})
        except InvalidAccessToken:
            raise ValueError from InvalidAccessToken
