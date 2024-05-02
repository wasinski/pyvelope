from collections import defaultdict
from collections.abc import Callable
from typing import get_type_hints

from attrs import evolve

from pyvelope._pyvelope.abstractions.message_bus import Consumer
from pyvelope._pyvelope.abstractions.messages import Envelope, TMsg


def get_consumer_envelope_wrapped_type(
    func: Callable[[Consumer[TMsg], Envelope[TMsg]], None]
    | Callable[[Envelope[TMsg]], None],
) -> type[TMsg]:
    """Get the type of the message wrapped in the Envelope from the Consumer's
    .consume method signature."""
    hints = get_type_hints(func)
    param_type = hints.get("envelope") or hints.get("message") or hints["msg"]
    if hasattr(param_type, "__args__"):
        return param_type.__args__[0]
    raise ValueError("Consumer must have a message type")


def serialize(envelope: Envelope[TMsg], msg_type: type[TMsg]) -> Envelope[TMsg]:
    return evolve(envelope, message=msg_type(**envelope.message))


# simple, poorly implemented, just to showcase the concept
class MessageDispatcher:
    def __init__(
        self, consumer_provider: Callable[[type[Consumer[TMsg]]], Consumer[TMsg]]
    ):
        self.consumer_provider = consumer_provider
        self.consumers: dict[str, list[type[Consumer[TMsg]]]] = defaultdict(list)

    def register_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        key: type[TMsg] = get_consumer_envelope_wrapped_type(consumer_type.consume)  # type: ignore[arg-type] # mypy bug?
        self.consumers[key.__name__].append(consumer_type)

    def dispatch(self, message: Envelope[TMsg]) -> None:
        print(f"Dispatching message: {message}")
        message_key = message.message_type
        for consumer_type in self.consumers[message_key]:
            consumer = self.consumer_provider(consumer_type)
            serialized_message = serialize(
                message, get_consumer_envelope_wrapped_type(consumer.consume)
            )
            consumer.consume(serialized_message)
