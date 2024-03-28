from dataclasses import dataclass

from pyvelope._pyvelope.abstractions.message_bus import Consumer, MessageBus, SendAddress
from pyvelope._pyvelope.abstractions.messages import Envelope
from pyvelope._pyvelope.implementations.eventbridge.transport import EventbridgeTransport
from pyvelope._pyvelope.implementations.sqs.transport import SqsQueueUrl, SqsTransport


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


if __name__ == "__main__":
    # setup mocks
    from unittest.mock import Mock
    from pyvelope._pyvelope.implementations.message_bus import MessageBus

    EXAMPLE_SQS_QUEUE_URL = "https://sqs.us-east-1.amazonaws.com/123456789012/my_queue"

    sqs_client = Mock()
    eventbridge_client = Mock()

    message_bus = MessageBus()
    sqs_transport = SqsTransport(sqs_client)
    sqs_transport.bind_consumer(ConsumerOfSecondCommand)
    sqs_transport.bind_msg_type(MyCommand)
    sqs_transport.bind_msg_type(MyEvent, queue_name="special-my-event-queue")

    eventbridge_transport = EventbridgeTransport(
        eventbridge_client, default_bus="default_bus"
    )
    eventbridge_transport.bind_msg_type(MyEvent)

    message_bus.add_transport(sqs_transport)
    message_bus.add_transport(eventbridge_transport)

    message_bus.publish(MyEvent("Hello, World!"))
    assert eventbridge_client.put_events.call_count == 1
    assert sqs_client.send_message.call_count == 1

    message_bus.send(MyCommand("Hello, you!"))
    assert sqs_client.send_message.call_count == 2

    message_bus.send(MyCommand("Hello, you address!"), SqsQueueUrl(EXAMPLE_SQS_QUEUE_URL))
    assert sqs_client.send_message.call_count == 3

    message_bus.send(MyCommand("Hello, you bound address"), ConsumerOfSecondCommand)
    assert sqs_client.send_message.call_count == 4

    # fake an incoming message and send a reply, faking is needed to have it working without a "real" message bus
    received_message = Envelope(
        MyCommand("Hello, you!"), sender=SqsQueueUrl(EXAMPLE_SQS_QUEUE_URL)
    )
    message_bus.send(
        {"body": "Hi! Got your message"}, address=received_message.reply_address()
    )
    assert sqs_client.send_message.call_count == 5
