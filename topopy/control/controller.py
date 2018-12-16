import asyncio
from typing import Any, List

from .actor import Actor
from .client import ClientBase


class ActorController(Actor):
    __slots__ = ('_actors',)

    def __init__(self, loop: asyncio.BaseEventLoop, client: ClientBase,
                 id: Any=None, actors: List[Actor]=None):
        super().__init__(loop=loop, client=client, id=id)
        self._actors = actors


class SingleActorController(ActorController):
    __slots__ = ()

    def __init__(self, loop: asyncio.BaseEventLoop, client: ClientBase,
                 actor: Actor, id: Any=None):
        super().__init__(loop=loop, client=client, id=id, actors=[actor])

    @property
    def actor(self):
        return self._actors[0]
