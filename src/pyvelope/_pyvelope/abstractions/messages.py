from typing import Generic, Protocol, TypeVar, runtime_checkable

from attr import define


@runtime_checkable
class Address(Protocol):
    def __str__(self) -> str: ...


class Message(Protocol):
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
