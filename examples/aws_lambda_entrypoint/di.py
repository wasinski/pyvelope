import functools

from dependency_injector import containers, providers

from examples.aws_lambda_entrypoint.consumers import FirstSubscriber, SecondSubscriber
from pyvelope._pyvelope.abstractions.message_bus import Consumer
from pyvelope.simple import MessageDispatcher


class UnknownConsumerTypeError(Exception):
    def __init__(self, consumer_type: type[Consumer]) -> None:
        super().__init__(f"Unknown consumer type: {consumer_type}")


def get_consumer_from_service_provider(
    service_provider: "ServiceProvider", consumer_type: type[Consumer]
) -> Consumer:
    if consumer_type == FirstSubscriber:
        return service_provider().first_subscriber()
    if consumer_type == SecondSubscriber:
        return service_provider().second_subscriber()
    raise UnknownConsumerTypeError(consumer_type)


class ServiceProvider(containers.DeclarativeContainer):
    __self__ = providers.Self()

    message_dispatcher = providers.Singleton(
        MessageDispatcher,
        consumer_provider=functools.partial(get_consumer_from_service_provider, __self__),
    )
    first_subscriber = providers.Factory(FirstSubscriber)
    second_subscriber = providers.Factory(SecondSubscriber)
