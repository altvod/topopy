from topopy.control.message import Message


class MovementImpossible(Message):
    __slots__ = ()
    fields = ('loc',)


class InhabitCell(Message):
    __slots__ = ()
    fields = ('loc',)


class VacateCell(Message):
    __slots__ = ()
    fields = ('loc',)
