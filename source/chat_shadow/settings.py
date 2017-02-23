#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""

"""

import logging


GG_WEBSOCKET_LINK = 'ws://chat.goodgame.ru:8081/chat/websocket'

GG_USERS_IN_CHAT_LIMIT = 100

LOGGER_CONFIG = {
    'format': u'%(levelname)-8s :: %(funcName)-20s :: %(message)s',
    'level': logging.INFO,
}
