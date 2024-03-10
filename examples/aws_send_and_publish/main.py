from dataclasses import dataclass

from pyvelope.abstractions.message_bus import MessageBus, SendAddress
from pyvelope.abstractions.messages import Envelope


@dataclass
class MyEvent:
    body: str


@dataclass
class MyCommand:
    body: str


class PublisherService:
    def __init__(self, message_bus: MessageBus) -> None:
        self.message_bus = message_bus

    def publish_event(self) -> None:
        self.message_bus.publish(MyEvent("Hello, World!"))

    def send_command(self) -> None:
        self.message_bus.send(MyCommand("Hello, World!"), None)

    def send_to_address(self) -> None:
        self.message_bus.send(MyCommand("Hello, World!"), SendAddress("my_address"))

    def send_reply(self, received_message: Envelope[MyCommand]) -> None:
        self.message_bus.send(
            {"body": "Hi! Got your message"}, address=received_message.reply_address()
        )
