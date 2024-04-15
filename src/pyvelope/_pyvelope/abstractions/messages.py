from abc import ABC
from typing import Generic, NewType, Protocol, TypeVar

from attr import define


class Address(ABC):
    pass


class Message(ABC):
    pass


TMsg = TypeVar("TMsg", bound=Message)


@define
class Envelope(Generic[TMsg]):
    message_type: str
    message: TMsg
    sender: Address
    response_address: Address | None = None

    def reply_address(self) -> Address:
        assert self.response_address is not None
        return self.response_address
