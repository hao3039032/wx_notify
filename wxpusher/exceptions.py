#!/usr/bin/env python

class WxPusherException(Exception):
    """WxPusher specific base exception."""


class WxPusherNoneTokenException(WxPusherException):
    """Raised when both token and default token are None."""
