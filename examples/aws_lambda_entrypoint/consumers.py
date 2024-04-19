from attr import define

from pyvelope._pyvelope.abstractions.message_bus import Consumer
from pyvelope._pyvelope.abstractions.messages import Envelope


class AssertState:
    def __init__(self) -> None:
        self.consumer_1_called = False
        self.consumer_2_called = False


assert_state = AssertState()


@define
class MyEvent:
    body: str


class FirstSubscriber(Consumer[MyEvent]):
    def consume(self, msg: Envelope[MyEvent]) -> None:
        print(f"{self.__class__.__name__} Consumed: {msg.message.body}")
        assert_state.consumer_1_called = True


# One more Consumer for the same event to make things more interesting
class SecondSubscriber(Consumer[MyEvent]):
    def consume(self, msg: Envelope[MyEvent]) -> None:
        print(f"{self.__class__.__name__} Consumed: {msg.message.body}")
        assert_state.consumer_2_called = True
