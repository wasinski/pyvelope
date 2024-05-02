import json
from collections import defaultdict
from typing import Any

from attrs import asdict
from mypy_boto3_events import EventBridgeClient

from pyvelope._pyvelope.abstractions.message_bus import Consumer, Transport
from pyvelope._pyvelope.abstractions.messages import Address, Envelope, Message, TMsg
from pyvelope._pyvelope.implementations.sqs.transport import SqsQueueUrl

json_serializer = json


DEFAULT_BUS = object()  # !! type like autorecipient


class EventbridgeBusArn(Address):
    def __init__(self, arn: str) -> None:
        self.arn = arn


class EventbridgeTransport(Transport):
    def __init__(self, eventbridge_client: EventBridgeClient, default_bus: str) -> None:
        self.eventbridge_client = eventbridge_client
        self.default_bus = default_bus
        self.source = "pyvelope"  # !!
        self.bound: dict[str, list[str | object]] = defaultdict(list)  # !!

    def bind_msg_type(
        self, msg_type: type[TMsg], _: Any = None
    ) -> None:  # !! should be queue_name/bus_name
        self.bound[msg_type.__name__].append(DEFAULT_BUS)

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        msg_type = consumer_type.__args__[0]  # type: ignore[attr-defined]
        self.bound[msg_type.__name__].append(DEFAULT_BUS)

    def is_subscribed_to(self, message: Message) -> bool:
        return message.__class__.__name__ in self.bound

    def send(self, message: Message, context: object | None = None) -> None:
        # wrap message in envelope
        envelope = self.wrap_message(message, context)
        envelope_serialized = json_serializer.dumps(
            asdict(envelope), default=str
        )  # !! wrong serialization
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
        self, message: TMsg, context: object | None = None
    ) -> Envelope[TMsg]:
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

    def resolve_consumer_address(self, consumer: Consumer[Message]) -> str | None:
        raise NotImplementedError("to be refactored")
