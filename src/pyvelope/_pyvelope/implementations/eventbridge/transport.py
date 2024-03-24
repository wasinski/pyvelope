from pyvelope._pyvelope.abstractions.message_bus import Consumer, TMsg, Transport


class EventbridgeTransport(Transport):

    def __init__(self, eventbridge_client, default_bus: str) -> None:
        self.eventbridge_client = eventbridge_client
        self.default_bus = default_bus
        self.source = "pyvelope"  # !!

    def bind_msg_type(self, msg_type: type[object]) -> None:
        pass

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        pass

    def is_subscribed_to(self, message: object) -> bool:
        pass

    def send(self, message: object, context: object | None = None) -> None:
        # wrap message in envelope
        envelope = self.wrap_message(message, context)
        envelope_serialized = json_serializer.dumps(envelope)
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
