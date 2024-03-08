"""WXNotify service."""
from __future__ import annotations

import logging

import voluptuous as vol
from wxpusher import WxPusher

from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.typing import ConfigType

# The domain of your component. Should be equal to the name of your component.
DOMAIN = "wx_notify"
CONFIG_APPTOKEN = "app_token"
_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {DOMAIN: vol.Schema({vol.Required(CONFIG_APPTOKEN): cv.string})},
    extra=vol.ALLOW_EXTRA,
)


def setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the wx_notify service component."""
    app_token: str = config[DOMAIN][CONFIG_APPTOKEN]

    def wx_notify_msg(call: ServiceCall) -> None:
        """Notify msg via wx."""
        msg = call.data["message"]
        index = 1
        total = 0
        while True:
            query_res = WxPusher.query_user(index, 99, app_token)
            if query_res["code"] == 1000:
                data = query_res["data"]
                records = data["records"]
                uids = []
                for item in records:
                    uids.append(item["uid"])
                WxPusher.send_message(msg, uids=uids, token=app_token, summary=msg)
                total = total + len(records)
                if total >= data["total"]:
                    break
            else:
                break

    # Register our service with Home Assistant.
    hass.services.register(DOMAIN, "notify", wx_notify_msg)

    # Return boolean to indicate that initialization was successfully.
    return True
