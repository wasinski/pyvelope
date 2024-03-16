# Example for AWS setup using SQS & EventBride

Example showcases how to setup the MessageBus to be able to `.publish` and `.send` messages.

MessageBus is configured to use 2 transports, which use injected mocked `boto3` clients for SQS and Eventbridge. Consumers are mostly remote here (they are members of a different application), and are
bound by the message type to a specific transport, with the exception of `ConsumerOfSecondCommand`. This shows that MessageBus by default requires only "consumer side" configuration to be able to route messages.

Also note that the `.publish` method published a bounded messages to all subscribed parties, in this example it is both declared transports.

Queues, with the exception of specified `special-my-event-queue` are named automatically, based on the message name.

!! what about the bus name?
