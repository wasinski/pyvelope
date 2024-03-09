from dataclasses import dataclass

from pyvelope.abstractions.messages import Envelope, TMsg


@dataclass
class EnvelopeRecord(Envelope[TMsg]):
    message_type: str
    message: TMsg
