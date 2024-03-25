from pyvelope._pyvelope.abstractions.message_bus import (
    MessageBus as IMessageBus,
    SendAddress,
)


class MessageBus(IMessageBus):
    def __init__(self):
        self._transports = []
        self.context = None

    def add_transport(self, transport) -> None:
        self._transports.append(transport)

    def publish(self, message: object) -> None:
        breakpoint()
        for transport in self._transports:
            if transport.is_subscribed_to(message):
                transport.send(message, self.context)

    # for later
    def send(self, message: object, address: SendAddress | None = None) -> None:
        if address:
            for transport in self._transports:
                if transport.supports_address(address):
                    transport.send(message, self.context)
                    return
            raise AssertionError(f"Address {address} not supported by any transport")

        for transport in self._transports:
            if transport.has_matching_consumer(message):
                transport.send(message, self.context)
                # ? if many consumers found, then maybe raise an exception?
                return
