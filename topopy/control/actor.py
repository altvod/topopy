import asyncio
import uuid
from typing import Any, Awaitable, Dict, Optional, Type  # noqa

from aiochannel import Channel as AioChannel

from topopy.utils.methdispatch import methdispatch
from .message import Message
from .client import ClientBase


class ActorDispatcherBase:
    """Routes events to :class:`Actor` methods"""
    def __init__(self, actor):
        self.actor = actor

    @methdispatch
    def dispatch(self, message: Message) -> Optional[Awaitable]:
        """Should return an awaitable or None"""
        raise RuntimeWarning('Unhandled message: {}'.format(message))


class Actor:
    __slots__ = ('id', 'client', 'queues', 'loop', 'tasks', 'dispatcher')

    __dispatcher_class__ = ActorDispatcherBase

    @staticmethod
    def generate_id():
        return uuid.uuid4()

    def __init__(self, loop: asyncio.BaseEventLoop, client: ClientBase,
                 id: Any=None):
        self.loop = loop
        self.id = id or self.generate_id()
        self.client = client
        self.queues = {}  # type: Dict[Type[Message], AioChannel]
        self.tasks = {}  # type: Dict[Type[Message], asyncio.Task]
        self.dispatcher = self.__dispatcher_class__(self)

    async def subscribe(self, channel: str):
        """
        Subscribe actor to an event channel.
        Can be awaited in any event loop or thread
        that can differ from the actor's own
        """
        self.queues[channel] = await self.client.subscribe(channel)
        self.schedule_channel_handler(channel)

    async def handle_message(self, message: Message):
        """
        Run the action required for this type of message
        """
        action = self.dispatcher.dispatch(message)
        if action is not None:
            await action

    async def handle_queue(self, queue: AioChannel):
        """
        Handle all events from queue asynchronously
        """
        async for message in queue:
            await self.handle_message(message)

    def _schedule_channel_handler_unsafe(self, channel: str):
        """
        Reschedule waiting for a new message in channel.
        Thread-unsafe
        """
        self.tasks[channel] = self.loop.create_task(
            self.handle_queue(self.queues[channel])
        )

    def schedule_channel_handler(self, channel: str):
        """
        Reschedule waiting for a new message in channel.
        Thread-safe
        """
        self.loop.call_soon_threadsafe(
            self._schedule_channel_handler_unsafe(channel)
        )

    async def unsubscribe(self, channel: str):
        self.queues[channel].close()
        del self.queues[channel]

    async def send(self, channel: str, message: Message):
        await self.client.send(channel=channel, message=message)

    def send_nowait(self, channel: str, message: Message):
        self.client.send_nowait(channel=channel, message=message)
