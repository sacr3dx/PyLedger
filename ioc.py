from uuid import uuid4

from dishka import Provider, Scope, provide

from application import interfaces


class AppProvide(Provider):

    @provide(scope=Scope.APP)
    def get_uuid_generator(self) -> interfaces.GenerateUUID:
        return uuid4
