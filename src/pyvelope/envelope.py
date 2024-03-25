from dataclasses import dataclass

from pyvelope._pyvelope.abstractions.message_bus import TMsg
from pyvelope._pyvelope.abstractions.messages import Envelope


@dataclass
class EnvelopeRecord(Envelope[TMsg]):
    message_type: str
    message: TMsg
