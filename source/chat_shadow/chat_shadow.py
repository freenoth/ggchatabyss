#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

"""

"""

import asyncio
import json
import logging
import websockets
import re

from .settings import GG_WEBSOCKET_LINK, GG_USERS_IN_CHAT_LIMIT


class GGChatAbyss(object):
    def __init__(self, event_loop):
        super(GGChatAbyss, self).__init__()
        self.loop = event_loop
        self.websocket = None

        self.logger = logging.getLogger(__name__)

        self.channels = set()
        self.need_more_channels = False
        self.more_channels_start = 0

    def __del__(self):
        self.loop.close()

    @staticmethod
    def build_message(message_type, **kwargs):
        message = dict()
        message['type'] = message_type
        message['data'] = dict(**kwargs)
        return json.dumps(message)

    @staticmethod
    def cid(channel_id):
        cid = str(channel_id)
        return int(cid) if cid.isnumeric() else cid

    @staticmethod
    def parse_smiles(text):
        return []

    def save_data(self, channel_id, user_id, user_name, smiles):
        self.logger.info('get smiles %s', smiles)

    async def cmd_connect_to_channel(self, channel_id):
        if channel_id not in self.channels:
            message = self.build_message('join', channel_id=channel_id)
            await self.websocket.send(message)

    async def cmd_disconnect_from_channel(self, channel_id):
        if channel_id in self.channels:
            message = self.build_message('unjoin', channel_id=channel_id)
            await self.websocket.send(message)

    async def cmd_get_channel_list(self, start=0, count=50):
        self.logger.info('Get channel list from %d count %s', start, count)
        message = self.build_message('get_channels_list', start=start, count=count)
        await self.websocket.send(message)

    async def manage_channels(self):
        self.logger.info('Start manage channels')
        try_count = 0
        while True:
            if try_count == 0:
                try_count = 60
                await self.cmd_get_channel_list()
            elif self.need_more_channels:
                await self.cmd_get_channel_list(start=self.more_channels_start)
            try_count -= 1
            await asyncio.sleep(10)

    async def read_messages(self):
        self.logger.info('Start read messages!')
        while True:
            raw_response = await self.websocket.recv()
            response = json.loads(raw_response)

            if response['type'] == 'error':
                asyncio.ensure_future(self.process_error(response['data']))
            elif response['type'] == 'success_join':
                asyncio.ensure_future(self.process_success_join(response['data']))
            elif response['type'] == 'success_unjoin':
                asyncio.ensure_future(self.process_success_unjoin(response['data']))
            elif response['type'] == 'channels_list':
                asyncio.ensure_future(self.process_channels_list(response['data']))
            elif response['type'] == 'channel_counters':
                asyncio.ensure_future(self.process_counters(response['data']))
            elif response['type'] == 'message':
                asyncio.ensure_future(self.process_message(response['data']))
            else:
                self.logger.warning('unhandled message > %s', response)

    async def process_message(self, data):
        self.logger.warning(data)
        smiles = self.parse_smiles(data['text'])
        if smiles:
            self.save_data(self.cid(data['channel_id']), data['user_id'], data['user_name'], smiles)

    async def process_counters(self, data):
        if int(data['users_in_channel']) < GG_USERS_IN_CHAT_LIMIT:
            asyncio.ensure_future(self.cmd_disconnect_from_channel(self.cid(data['channel_id'])))

    async def process_channels_list(self, data):
        self.need_more_channels = True

        for channel in data['channels']:
            if self.cid(channel['channel_id']) not in self.channels and int(channel['users_in_channel']) >= GG_USERS_IN_CHAT_LIMIT:
                asyncio.ensure_future(self.cmd_connect_to_channel(self.cid(channel['channel_id'])))
            elif self.need_more_channels:
                self.need_more_channels = False
                self.more_channels_start = 0

        if self.need_more_channels:
            self.more_channels_start += len(data['channels'])

    async def process_error(self, data):
        self.logger.warning('Catch error message %s', json.dumps(data))
        if 0 <= data['error_num'] <= 100:  # bad requests
            pass
        elif 101 <= data['error_num'] <= 200:  # bad data
            pass
        elif 201 <= data['error_num'] <= 300:  # bad rights
            pass
        else:
            self.logger.error('Unknown error code %s', json.dumps(data))

    async def process_success_join(self, data):
        self.channels.add(self.cid(data['channel_id']))
        self.logger.info('Success connect to %s, streamer = %s', data['channel_id'], data['channel_streamer']['name'])

    async def process_success_unjoin(self, data):
        self.channels.remove(self.cid(data['channel_id']))
        self.logger.info('Success disconnect from channel %s', data['channel_id'])

    async def start_async(self):
        self.websocket = await websockets.connect(GG_WEBSOCKET_LINK)

        # get the hello-message
        response = await self.websocket.recv()
        json_response = json.loads(response)

        if json_response['type'] != 'welcome':
            self.logger.critical('Bad hello message (not "welcome") = %s', response)
            self.loop.stop()
            return
        self.logger.info('Start with %s', json_response['data'])

        asyncio.ensure_future(self.read_messages())
        asyncio.ensure_future(self.manage_channels())

    def start(self):
        asyncio.ensure_future(self.start_async())
        self.loop.run_forever()
