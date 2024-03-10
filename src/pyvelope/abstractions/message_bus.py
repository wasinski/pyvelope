from typing import Protocol, TypeVar

from pyvelope.abstractions.messages import Envelope

TMsg = TypeVar("TMsg")
SendAddress = str  # TODO: Define the AddressEndpoint type


class Consumer(Protocol[TMsg]):
    def consume(self, envelope: Envelope[TMsg]) -> None: ...


class MessageBus(Protocol):
    def publish(self, message: TMsg) -> None:
        """Publish a message to the message bus.

        Message will be delivered in a PubSub manner to all consumers that are subscribed
        to this message type.
        """

    def send(self, message: TMsg, address: SendAddress | None) -> None:
        """Send a message to a specific address.

        If the address is None the MessageBus will try to resolve it from the message type.
        This means that you could have many consumers for the same message type, but .send
        method should be used when you want to send a message to a specific consumer.

        Exactly one matched AddressPoint is expected, thus when the automatic address resolution founds none,
        or more than one consumer for the message type an error is raised.
        """
