from examples.aws_lambda_entrypoint.consumers import (
    FirstSubscriber,
    SecondSubscriber,
    assert_state,
)
from examples.aws_lambda_entrypoint.di import ServiceProvider
from examples.aws_lambda_entrypoint.utils import eventbridge_event_factory
from pyvelope._pyvelope.abstractions.messages import Envelope
from pyvelope.envelope import EnvelopeRecord


def get_service_provider() -> ServiceProvider:
    global service_provider  # noqa: PLW0603
    if not service_provider:
        service_provider = ServiceProvider()
    return service_provider


def envelope_from_eventbridge(event: dict) -> Envelope[object]:
    return EnvelopeRecord(
        message_type=event["detail-type"],
        message=event["detail"]["message"],
    )


def lambda_entrypoint(event, _context, service_provider=None) -> object | None:
    message = envelope_from_eventbridge(event)
    service_provider = get_service_provider()
    message_dispatcher = service_provider.message_dispatcher()
    message_dispatcher.dispatch(message)


if __name__ == "__main__":
    # setup globals
    service_provider = None

    # configure the message dispatcher - it's a singleton
    message_dispatcher = get_service_provider().message_dispatcher()
    message_dispatcher.register_consumer(FirstSubscriber)
    message_dispatcher.register_consumer(SecondSubscriber)

    # handle the event
    lambda_entrypoint(eventbridge_event_factory(), {})

    # assert the consumers were called
    assert assert_state.consumer_1_called
    assert assert_state.consumer_2_called
