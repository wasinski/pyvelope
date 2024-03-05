from typing import Protocol

from pyvelope.primitives.messages import OutboxMessage, TMsg


class MessageRelay(Protocol):
    def relay(self, message: OutboxMessage[TMsg]) -> None: ...
