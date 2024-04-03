from pyvelope._pyvelope.abstractions.message_bus import (
    Consumer,
    MessageBus as IMessageBus,
)
from pyvelope._pyvelope.abstractions.messages import Address


class MessageBus(IMessageBus):
    def __init__(self):
        self._transports = []
        self.context = None

    def add_transport(self, transport) -> None:
        self._transports.append(transport)

    def publish(self, message: object) -> None:
        for transport in self._transports:
            if transport.is_subscribed_to(message):
                transport.send(message, self.context)

    def send(self, message: object, address: Address | Consumer | None = None) -> None:
        if address and isinstance(address, Address):
            for transport in self._transports:
                if transport.supports_address(address):
                    # ? should we pass the address to the transport?
                    # if so then maybe signature should be changed?
                    # and routing should be made differently, on a separate api?
                    transport.send(message, self.context)
                    return
            raise AssertionError(f"Address {address} not supported by any transport")

        for transport in self._transports:
            if transport.is_subscribed_to(message):
                transport.send(message, self.context)
                # ? if many consumers found, then maybe raise an exception?
                return
