from collections import defaultdict
from pyvelope._pyvelope.abstractions.message_bus import Consumer
from pyvelope._pyvelope.abstractions.messages import Envelope, Address, Message, TMsg
import json

from attrs import asdict

from pyvelope._pyvelope.implementations.sqs.transport import SqsQueueUrl


json_serializer = json


DEFAULT_BUS = object()


class EventbridgeBusArn(Address):
    def __init__(self, arn: str) -> None:
        self.arn = arn


class EventbridgeTransport:
    def __init__(self, eventbridge_client, default_bus: str) -> None:
        self.eventbridge_client = eventbridge_client
        self.default_bus = default_bus
        self.source = "pyvelope"  # !!
        self.bound: dict[str, list[str]] = defaultdict(list)  # !!

    def bind_msg_type(self, msg_type: type[object]) -> None:
        self.bound[msg_type.__name__].append(DEFAULT_BUS)

    def bind_consumer(self, consumer_type: type[Consumer[Message]]) -> None:
        msg_type = consumer_type.__args__[0]  # !! to be fixed
        self.bound[msg_type.__name__].append(DEFAULT_BUS)

    def is_subscribed_to(self, message: Message) -> bool:
        return message.__class__.__name__ in self.bound

    def send(self, message: Message, context: object | None = None) -> None:
        # wrap message in envelope
        envelope = self.wrap_message(message, context)
        envelope_serialized = json_serializer.dumps(asdict(envelope))
        self.eventbridge_client.put_events(
            Entries=[
                {
                    "Source": self.source,
                    "DetailType": "pyvelope.message_type",
                    "Detail": envelope_serialized,
                    "EventBusName": self.default_bus,
                }
            ]
        )

    def wrap_message(
        self, message: Message, context: object | None = None
    ) -> Envelope[Message]:
        # ?? sender in general needs some rethinking...
        # maybe it's better to have an explicit "respond_to" field?
        # but that might not work in all contexts
        return Envelope(
            message_type=type(message).__name__,
            message=message,
            sender=SqsQueueUrl("invalid"),
        )

    def supports_address(self, address: Address) -> bool:
        return False
