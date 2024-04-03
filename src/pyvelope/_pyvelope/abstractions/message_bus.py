from typing import Protocol, TypeVar

from pyvelope._pyvelope.abstractions.messages import Envelope, Address


TMsg = TypeVar("TMsg")


class Consumer(Protocol[TMsg]):
    def consume(self, envelope: Envelope[TMsg]) -> None: ...


class ConsumerAddressResolver(Protocol):
    def resolve_address(self, consumer: Consumer) -> str:
        """Resolve the address of the consumer.

        This method should return the address of the consumer, which is used to send
        messages to the consumer.
        """


class Address:
    pass


class Consumer(Protocol[TMsg]):
    def consume(self, envelope: Envelope[TMsg]) -> None: ...


class MessageBus(Protocol):
    def publish(self, message: TMsg) -> None:
        """Publish a message to the message bus.

        Message will be delivered in a PubSub manner to all consumers that are subscribed
        to this message type.
        """

    def send(self, message: TMsg, address: Address | None = None) -> None:
        """Send a message to a specific address.

        If the address is None the MessageBus will try to resolve it from the message type.
        This means that you could have many consumers for the same message type, but .send
        method should be used when you want to send a message to a specific consumer.

        Exactly one matched AddressPoint is expected, thus when the automatic address resolution founds none,
        or more than one consumer for the message type an error is raised.
        """


class QueueRouter(ConsumerAddressResolver):
    def bind_msg_type(
        self, msg_type: type[object], queue_name: str | None = None
    ) -> None:
        """Bind a message type.

        queue_name is optional, when not given the router will use a default queue name (or generate one).
        """

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        """Bind a consumer to the router."""
