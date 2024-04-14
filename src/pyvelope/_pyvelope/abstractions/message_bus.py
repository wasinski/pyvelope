from typing import Generic, NewType, Protocol, TypeVar

from pyvelope._pyvelope.abstractions.json import Json
from pyvelope._pyvelope.abstractions.messages import Envelope, Address, Message


TMsg = TypeVar("TMsg", Message)
TMsg_In = TypeVar("TMsg_In", Message, contravariant=True)


class Consumer(Protocol[TMsg]):
    def consume(self, envelope: Envelope[TMsg]) -> None: ...


class ConsumerAddressResolver(Protocol):
    def resolve_address(self, consumer: Consumer[Message]) -> str:
        """Resolve the address of the consumer.

        This method should return the address of the consumer, which is used to send
        messages to the consumer.
        """


AutoRecipient = NewType("AutoRecipient", object)
AUTO_RECIPIENT = AutoRecipient(object())
Recipient = Address | Consumer[TMsg]


class Sender(Protocol[TMsg]):
    def send(
        self, message: TMsg, recipient: Recipient[TMsg] | AutoRecipient = AUTO_RECIPIENT
    ) -> None:
        """Send a message to a single Recipient.

        If the recipient is AUTO_RECIPIENT the MessageBus will try to resolve it from the message type (or raise).
        This means that you could have many consumers for the same message type, but .send
        method should be used when you want to send a message to a specific consumer.

        When making automatic recipient resolution finding exactly one address is expected, thus if none,
        or more than one address if found for the message type an error is raised.
        """


class Publisher(Protocol[TMsg_In]):
    def publish(self, message: TMsg_In) -> None:
        """Publish a message to the message bus.

        Message will be delivered in a PubSub manner to all consumers that are subscribed
        to this message type.
        """


class MessageBus(Sender[TMsg], Publisher[TMsg], Protocol): ...


class QueueRouter(ConsumerAddressResolver, Protocol):
    def bind_msg_type(self, msg_type: type[TMsg], queue_name: str | None = None) -> None:
        """Bind a message type.

        queue_name is optional, when not given the router will use a default queue name (or generate one).
        """

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        """Bind a consumer to the router."""

    def supports_address(self, address: Address) -> bool: ...

    def is_subscribed_to(self, message: TMsg) -> bool: ...


class Transport(QueueRouter, Protocol):
    def send(self, message: TMsg, context: object | None = None) -> None: ...

    def wrap_message(
        self, message: TMsg, context: object | None = None
    ) -> Envelope[TMsg]: ...
