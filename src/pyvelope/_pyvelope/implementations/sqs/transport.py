from typing import Protocol

from pyvelope._pyvelope.abstractions.message_bus import Consumer, QueueRouter


class SqsTransport(QueueRouter):
    def bind_consumer(self, consumer_type: type[Consumer]) -> None:
        """Bind a consumer to the transport.

        This means that this transport will be used to deliver messages to this consumer,
        based on the bound message type.

        Method can be used when a consumer is part of the same codebase as the producer,
        thus can be directly referenced.
        """

    def bind_msg_type(self, msg_type: type[object]) -> None:
        """Bind a message type to this transport.

        This means that this transport will be used to deliver messages of this type to
        consumers that await this message type.

        Method can be used when a consumer is not part of the same codebase as the producer.
        """

    def resolve_consumer_address(self, consumer: "Consumer") -> str | None:
        """Resolve the address of the consumer.

        This method should return the address of the consumer, which is used to send
        messages to the consumer.
        """
    
    def resolve_message_address(self, message: object) -> str | None:
        """Resolve the address of the message.

        This method should return the address of the message, which is used to send
        messages to the consumer.
        """
