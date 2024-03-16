from typing import Protocol


class Transport(Protocol):
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
