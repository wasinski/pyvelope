from attrs import define

from pyvelope import Consumer, Envelope
from pyvelope.aws import EventbridgeTransport, SqsQueueUrl, SqsTransport


@define
class MyEvent:
    body: str


@define
class MyCommand:
    body: str


@define
class MySecondCommand:
    body: str


class ConsumerOfSecondCommand(Consumer[MySecondCommand]):
    def consume(self, message: Envelope[MySecondCommand]) -> None:
        print(f"Received message: {message.message.body}")


# setup mocks
from unittest.mock import Mock

from pyvelope import MessageBus

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
    "MyCommand",
    "Hello, you!",
    sender=SqsQueueUrl(EXAMPLE_SQS_QUEUE_URL),
    response_address=SqsQueueUrl(EXAMPLE_SQS_QUEUE_URL),
)
message_bus.send(
    {"body": "Hi! Got your message"}, recipient=received_message.reply_address()
)
assert sqs_client.send_message.call_count == 5
