from typing import Any

from pyvelope._pyvelope.abstractions.message_bus import (
    AUTO_RECIPIENT,
    AutoRecipient,
    Consumer,
    Transport,
)
from pyvelope._pyvelope.abstractions.message_bus import (
    MessageBus as IMessageBus,
)
from pyvelope._pyvelope.abstractions.messages import Address, Message
from pyvelope._pyvelope.exceptions import ConfigurationError


class MessageBus(IMessageBus):
    def __init__(self) -> None:
        self._transports: list[Transport] = []
        self.context = None

    def add_transport(self, transport: Transport) -> None:
        self._transports.append(transport)

    def publish(self, message: Message) -> None:
        for transport in self._transports:
            if transport.is_subscribed_to(message):
                transport.send(message, self.context)

    def send(
        self,
        message: Message,
        recipient: Address | type[Consumer[Any]] | AutoRecipient = AUTO_RECIPIENT,
    ) -> None:
        if recipient and isinstance(recipient, Address):
            for transport in self._transports:
                if transport.supports_address(recipient):
                    # ? should we pass the address to the transport?
                    # if so then maybe signature should be changed?
                    # and routing should be made differently, on a separate api?
                    transport.send(message, self.context)
                    return
            raise ConfigurationError.address_not_supported(str(recipient))

        for transport in self._transports:
            if transport.is_subscribed_to(message):
                transport.send(message, self.context)
                # ? if many consumers found, then maybe raise an exception?
                return
