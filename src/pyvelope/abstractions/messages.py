from typing import Protocol, TypeVar

TMsg = TypeVar("TMsg")


class Envelope(Protocol[TMsg]):
    message_type: str
    message: TMsg
