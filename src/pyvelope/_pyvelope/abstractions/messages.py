from abc import ABC
from typing import Generic, Protocol, TypeVar

from attr import define


TMsg = TypeVar("TMsg")


class Address(ABC):
    pass


@define
class Envelope(Generic[TMsg]):
    message_type: str
    message: TMsg
    sender: Address
    response_address: Address | None = None

    def reply_address(self) -> Address:
        assert self.response_address is not None
        return self.response_address
