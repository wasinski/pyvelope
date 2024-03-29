from abc import ABC
from typing import Protocol, TypeVar


TMsg = TypeVar("TMsg")


class SendAddress(ABC):
    pass


class Envelope(Protocol[TMsg]):
    message_type: str
    message: TMsg
    sender: SendAddress
