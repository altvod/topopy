import asyncio
from typing import Dict, List  # noqa

from aiochannel import Channel

from .message import Message


class ClientBase:
    ALL = '*'

    def __init__(self, loop: asyncio.BaseEventLoop):
        self.loop = loop
        self.subscribers = {}  # type: Dict[str, List[Channel]]

    async def subscribe(self, channel: str) -> Channel:
        if channel not in self.subscribers:
            self.subscribers[channel] = []

        new_channel = Channel(loop=self.loop)
        self.subscribers[channel].append(new_channel)
        return new_channel

    async def send(self, channel: str, message: Message):
        for subscriber in self.subscribers[self.ALL]:
            await subscriber.put(message)

        for subscriber in self.subscribers[channel]:
            await subscriber.put_nowait(message)

    def send_nowait(self, channel: str, message: Message):
        for subscriber in self.subscribers[self.ALL]:
            subscriber.put_nowait(message)

        for subscriber in self.subscribers[channel]:
            subscriber.put_nowait(message)
