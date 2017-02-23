#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""

"""

import asyncio
import logging
from chat_shadow import GGChatAbyss
from settings import LOGGER_CONFIG


def _main():
    loop = asyncio.get_event_loop()
    gg = GGChatAbyss(event_loop=loop)
    gg.start()


if __name__ == '__main__':
    logging.basicConfig(**LOGGER_CONFIG)
    _main()
