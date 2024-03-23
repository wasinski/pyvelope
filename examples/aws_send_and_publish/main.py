from dataclasses import dataclass

from pyvelope._pyvelope.abstractions.message_bus import Consumer, MessageBus, SendAddress
from pyvelope._pyvelope.abstractions.messages import Envelope

@dataclass
class MyEvent:
    body: str


@dataclass
class MyCommand:
    body: str


@dataclass
class MySecondCommand:
    body: str


class ConsumerOfSecondCommand(Consumer[MySecondCommand]):
    def consume(self, message: Envelope[MySecondCommand]) -> None:
        print(f"Received message: {message.body}")


class PublisherService:
    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus = message_bus

    def publish_event(self) -> None:
        self.message_bus.publish(MyEvent("Hello, World!"))

    def send_command(self) -> None:
        self.message_bus.send(MyCommand("Hello, you!"))

    def send_to_address(self) -> None:
        self.message_bus.send(MyCommand("Hello, you address!"), SendAddress("my_address"))

    def send_to_bound_address(self) -> None:
        self.message_bus.send(
            MyCommand("Hello, you bound address"), SendAddress(ConsumerOfSecondCommand)
        )

    def send_reply(self, received_message: Envelope[MyCommand]) -> None:
        self.message_bus.send(
            {"body": "Hi! Got your message"}, address=received_message.reply_address()
        )


if __name__ == "__main__":
    # setup mocks
    from unittest.mock import Mock
    from pyvelope._pyvelope.implementations.message_bus import MessageBus

    sqs_client = Mock()
    eventbridge_client = Mock()

    message_bus = MessageBus()
    sqs_transport = SqsTransport()
    sqs_transport.bind_consumer(ConsumerOfSecondCommand)
    sqs_transport.bind_msg_type(MyCommand)
    sqs_transport.bind_msg_type(MyEvent, queue_name="special-my-event-queue")

    eventbridge_transport = EventBridgeTransport(eventbridge_client)
    eventbridge_transport.bind_msg_type(MyEvent)

    message_bus.add_transport(sqs_transport)
    message_bus.add_transport(eventbridge_transport)

    publisher_service = PublisherService(message_bus)

    publisher_service.publish_event()  # `publish` sends event to all subscribers
    assert eventbridge_client.put_events.call_count == 1
    assert sqs_client.send_message.call_count == 1

    publisher_service.send_command()
    assert sqs_client.send_message.call_count == 2

    publisher_service.send_to_address()
    assert sqs_client.send_message.call_count == 3

    publisher_service.send_to_bound_address()
    assert sqs_client.send_message.call_count == 4

    # fake an incoming message and send a reply, faking is needed to have it working without a "real" message bus
    received_message = Envelope(
        MyCommand("Hello, you!"), sender=SendAddress("my_address")
    )
    publisher_service.send_reply(received_message=received_message)
    assert sqs_client.send_message.call_count == 5
