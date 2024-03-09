from typing import Protocol, TypeVar

from pyvelope.abstractions.messages import Envelope

TMsg = TypeVar("TMsg")


class Consumer(Protocol[TMsg]):
    def consume(self, envelope: Envelope[TMsg]) -> None: ...


class MessageBus(Protocol):
    def publish(self, message: TMsg) -> None: ...

    def send(self, message: TMsg) -> None: ...
