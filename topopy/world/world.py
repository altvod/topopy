import asyncio
from collections import namedtuple
from typing import Any, Awaitable, Dict, List, Optional, Union  # noqa

from topopy.control.actor import Actor, ActorDispatcherBase, methdispatch
from topopy.control.client import ClientBase
from topopy.control.message import Message
from topopy.primitives.location import Location
from topopy.primitives.topology import Topology
from topopy.primitives.movement import MovementStrategy
from topopy.utils.methdispatch import methdispatch
from . import messages


class TopoActor(Actor):
    __slots__ = ('_loc', '_movement_strategies', '_world')

    def __init__(
            self,
            *args,
            world: 'World',
            loc=None,
            movement_strategies: Dict[Any, MovementStrategy]=None,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self._world = world
        self._loc = loc
        self._movement_strategies = movement_strategies or {}

    @property
    def loc(self):
        return self.loc

    def inhabit_location(self, loc: Location):
        self.send(messages.InhabitCell(loc=loc))

    def vacate_location(self, loc: Location):
        self.send(messages.VacateCell(loc=loc))

    def check_movement(self, loc: Location) -> bool:
        """Check whether actor can move to a given location"""
        if not self._movement_strategies:
            return False

        old_world_loc = self._world.get_location(self.loc)
        new_world_loc = self._world.get_location(loc)
        for topo, movement in self._movement_strategies.items():
            passability = movement.get_passability(
                from_loc=self._loc,
                to_loc=loc,
                from_tile=old_world_loc.tiles[topo],
                to_tile=new_world_loc.tiles[topo]
            )
            if passability is None:
                return False

        return True

    def move_to(self, loc: Location):
        """
        Move to a new cell at the given location
        """
        if self.loc is not None:
            if not self.check_movement(loc):
                return
            self.vacate_location(self.loc)

        self.inhabit_location(loc)
        self._loc = loc


WorldLocation = namedtuple(
    'WorldLocation', (
        'actors',
        'tiles',
    )
)


class WorldBase(Actor):
    def __init__(
            self,
            loop: asyncio.BaseEventLoop,
            client: ClientBase,
            topologies: Dict[Any, Topology],
            actors: Union[List[Actor], Dict[Actor]]
    ):
        super().__init__(loop=loop, client=client)

        if isinstance(actors, list):
            actors = {a.id: actors for a in actors}

        self.topologies = topologies
        self.actors = actors
        self.actors_by_loc = {}  # type: Dict[Location, List[Any]]

    def get_location(self, loc: Location) -> WorldLocation:
        return WorldLocation(
            actors=self.actors_by_loc[loc],
            tiles={name: topo[loc] for name, topo in self.topologies},
        )

    def __getitem__(self, key):
        if isinstance(key, Location):
            return self.get_location(key)

        try:
            return self.actors[key]
        except KeyError:
            try:
                return self.topologies[key]
            except KeyError:
                raise KeyError(key)

    def __setitem__(self, key, item):
        if isinstance(item, Actor):
            self.actors[key] = item

        elif isinstance(item, Topology):
            self.topologies[key] = item

        else:
            raise TypeError(type(item))


class WorldDispatcher(ActorDispatcherBase):
    @property
    def world(self) -> 'WorldBase':
        return self.actor

    @methdispatch
    def dispatch(self, message: Message) -> Optional[Awaitable]:
        """Should return an awaitable or None"""
        return super().dispatch()

    @dispatch.register(messages.InhabitCell)
    def inhabit_cell(self, message):
        loc = message['loc']
        if loc not in self.world.actors_by_loc:
            self.world.actors_by_loc[loc] = []

        self.world.actors_by_loc[loc] = message.actor_id

    @dispatch.register(messages.VacateCell)
    def vacate_cell(self, message):
        loc = message['loc']
        self.world.actors_by_loc[loc].remove(message.actor_id)
        if not self.world.actors_by_loc[loc]:
            del self.world.actors_by_loc[loc]


class World(WorldBase):
    __dispatcher_class__ = WorldDispatcher
