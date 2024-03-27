from collections import defaultdict
from dataclasses import asdict
from typing import Protocol, get_type_hints
import json

from pyvelope._pyvelope.abstractions.messages import Envelope
from pyvelope.envelope import EnvelopeRecord
from pyvelope._pyvelope.abstractions.message_bus import Consumer, QueueRouter


json_serializer = json


def get_consumer_envelope_wrapped_type(func):
    """Get the type of the message wrapped in the Envelope from the Consumer's
    .consume method signature."""
    hints = get_type_hints(func)
    param_type = hints["message"]
    if hasattr(param_type, "__args__"):
        return param_type.__args__[0]
    return None


class SqsTransport(QueueRouter):
    def __init__(self, sqs_client) -> None:
        self.sqs_client = sqs_client
        self.source = "pyvelope"  # !!
        self.bound = defaultdict(list)  # !!

    def send(self, message: object, context: object | None = None) -> None:
        queue_url = "default_queue_url"  # !! to be fixed, taken from params or consumer
        envelope = self.wrap_message(message, context)
        envelope_serialized = json_serializer.dumps(asdict(envelope))

        self.sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=envelope_serialized,
            # MessageGroupId=message_group_id,
            # MessageDeduplicationId=message_deduplication_id,
            # MessageAttributes=message_attributes,
            # MessageSystemAttributes=message_system_attributes,
            # DelaySeconds=delay_seconds,
        )

    def is_subscribed_to(self, message: object) -> bool:
        return message.__class__.__name__ in self.bound

    def bind_consumer(self, consumer_type: type[Consumer]) -> None:
        """Bind a consumer to the transport.

        This means that this transport will be used to deliver messages to this consumer,
        based on the bound message type.

        Method can be used when a consumer is part of the same codebase as the producer,
        thus can be directly referenced.
        """
        msg_type = get_consumer_envelope_wrapped_type(consumer_type.consume)
        consumer_name = msg_type.__name__
        self.bound[consumer_name].append(consumer_name)

    def bind_msg_type(
        self, msg_type: type[object], queue_name: str | None = None
    ) -> None:
        """Bind a message type to this transport.

        This means that this transport will be used to deliver messages of this type to
        consumers that await this message type.

        Method can be used when a consumer is not part of the same codebase as the producer.
        """
        queue_name = queue_name or msg_type.__name__
        self.bound[msg_type.__name__].append(queue_name)

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

    def wrap_message(self, message: object, context: object | None = None) -> Envelope:
        return EnvelopeRecord(message_type=type(message).__name__, message=message)
