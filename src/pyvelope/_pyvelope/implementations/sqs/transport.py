from collections import defaultdict
from attrs import asdict
from typing import Callable, Protocol, get_type_hints
import json

from mypy_boto3_sqs import SQSClient
from pyvelope._pyvelope.abstractions.messages import Envelope, Address, Message, TMsg
from pyvelope._pyvelope.abstractions.message_bus import Consumer, QueueRouter
from pyvelope.simple import get_consumer_envelope_wrapped_type


json_serializer = json


class SqsQueueUrl(Address):
    def __init__(self, url: str) -> None:
        self.url = url


class SqsTransport(QueueRouter):
    def __init__(self, sqs_client: SQSClient) -> None:
        self.sqs_client = sqs_client
        self.source = "pyvelope"  # !!
        self.bound: dict[str, list[str]] = defaultdict(list)  # !!

    def send(self, message: Message, context: object | None = None) -> None:
        queue_url = "default_queue_url"  # !! to be fixed, taken from params or consumer
        envelope = self.wrap_message(message, context)
        envelope_serialized = json_serializer.dumps(asdict(envelope), default=str)  # !!

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

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        """Bind a consumer to the transport.

        This means that this transport will be used to deliver messages to this consumer,
        based on the bound message type.

        Method can be used when a consumer is part of the same codebase as the producer,
        thus can be directly referenced.
        """
        msg_type = get_consumer_envelope_wrapped_type(consumer_type.consume)
        consumer_name = msg_type.__name__  # plan is to use this as the queue name
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

    def resolve_consumer_address(self, consumer: "Consumer[TMsg]") -> str | None:
        """Resolve the address of the consumer.

        This method should return the address of the consumer, which is used to send
        messages to the consumer.
        """

    def resolve_message_address(self, message: TMsg) -> str | None:
        """Resolve the address of the message.

        This method should return the address of the message, which is used to send
        messages to the consumer.
        """

    def supports_address(self, address: Address) -> bool:
        if isinstance(address, SqsQueueUrl):
            return True
        return False

    def wrap_message(
        self, message: TMsg, context: object | None = None
    ) -> Envelope[TMsg]:
        return Envelope(
            message_type=type(message).__name__,
            message=message,
            sender=SqsQueueUrl("to-be-fixed"),
        )
