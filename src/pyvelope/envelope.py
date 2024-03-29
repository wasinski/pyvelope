from dataclasses import dataclass

from pyvelope._pyvelope.abstractions.message_bus import TMsg
from pyvelope._pyvelope.abstractions.messages import Envelope, SendAddress


@dataclass
class EnvelopeRecord(Envelope[TMsg]):
    message_type: str
    message: TMsg
    sender: SendAddress

    def reply_address(self) -> SendAddress:
        return self.sender
