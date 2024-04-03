from dataclasses import dataclass

from pyvelope._pyvelope.abstractions.message_bus import TMsg
from pyvelope._pyvelope.abstractions.messages import Envelope, Address


@dataclass
class EnvelopeRecord(Envelope[TMsg]):
    message_type: str
    message: TMsg
    sender: Address
    response_address: Address | None = None

    def reply_address(self) -> Address:
        assert self.response_address is not None
        return self.response_address
