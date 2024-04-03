from abc import ABC
from typing import Protocol, TypeVar


TMsg = TypeVar("TMsg")


class Address(ABC):
    pass


class Envelope(Protocol[TMsg]):
    message_type: str
    message: TMsg
    sender: Address
    response_address: Address | None
