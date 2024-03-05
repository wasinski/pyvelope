from typing import Protocol, TypeVar


class Message:
    pass


TMsg = TypeVar("TMsg")


class OutboxMessage(Protocol[TMsg]):
    message: TMsg
