from collections import defaultdict
from collections.abc import Callable
from attrs import evolve
from typing import get_type_hints

from pyvelope._pyvelope.abstractions.message_bus import Consumer, TMsg
from pyvelope._pyvelope.abstractions.messages import Envelope


def get_consumer_envelope_wrapped_type(func: Callable[[Envelope[TMsg]], None]) -> type[TMsg] | None:
    """Get the type of the message wrapped in the Envelope from the Consumer's
    .consume method signature."""
    hints = get_type_hints(func)
    param_type = hints["msg"]
    if hasattr(param_type, "__args__"):
        return param_type.__args__[0]
    return None


def serialize(envelope: Envelope[object], msg_type: type[object]) -> Envelope[object]:
    return evolve(envelope, message=msg_type(**envelope.message))


# simple, poorly implemented, just to showcase the concept
class MessageDispatcher:
    def __init__(self, consumer_provider: Callable[[type[Consumer[TMsg]]], Consumer[TMsg]]):
        self.consumer_provider = consumer_provider
        self.consumers: dict[str, list[Consumer[TMsg]]] = defaultdict(list)

    def register_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        key = get_consumer_envelope_wrapped_type(consumer_type.consume).__name__
        assert key is not None, "Consumer must have a message type"
        self.consumers[key].append(consumer_type)

    def dispatch(self, message: Envelope[object]) -> None:
        print(f"Dispatching message: {message}")
        message_key = message.message_type
        for consumer_type in self.consumers[message_key]:
            consumer = self.consumer_provider(consumer_type)
            serialized_message = serialize(
                message, get_consumer_envelope_wrapped_type(consumer.consume)
            )
            consumer.consume(serialized_message)
