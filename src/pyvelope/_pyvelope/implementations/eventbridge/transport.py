from pyvelope._pyvelope.abstractions.message_bus import Consumer, TMsg, Transport


class EventbridgeTransport(Transport):
    def bind_msg_type(self, msg_type: type[object]) -> None:
        pass

    def bind_consumer(self, consumer_type: type[Consumer[TMsg]]) -> None:
        pass
