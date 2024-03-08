"""WXNotify service."""
from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "wx_notify"
CONFIG_APPTOKEN = "app_token"
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema({
            vol.Required(CONFIG_APPTOKEN): cv.string
        })
    },
    extra=vol.ALLOW_EXTRA
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the wx_notify service component."""
    app_token: str = config[DOMAIN][CONFIG_APPTOKEN]
    _LOGGER.info("setup wx notify " + app_token)

    def wx_notify_msg(call: ServiceCall) -> None:
        """Notify msg via wx."""
        msg = call.data["message"]
        _LOGGER.info("Received data: " + msg)

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, "notify", wx_notify_msg)

    # Return boolean to indicate that initialization was successfully.
    return True
