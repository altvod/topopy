from topopy import exc


class Message(dict):
    __slots__ = ("actor_id",)

    fields = ()

    def __init__(self, actor, **kwargs):
        self.actor_id = actor.id
        if set(self.fields) != set(kwargs):
            raise exc.MessageFieldError(list(kwargs))

        super().__init__(**kwargs)

    def __str__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            super().__str__()
        )

    def __repr__(self):
        return '{}({})'.format(
            self.__class__.__name__,
            super().__repr__()
        )
