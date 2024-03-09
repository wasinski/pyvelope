# Pyvelope used in AWS Lambda

This example showcases how Pyvelope can be used in the entrypoint for AWS Lambda, where the Lambda Runtime is responsible for invoking the entrypoint and acknowledging the message (push-model).

The example uses `dependency-injector` to provide the required services (Consumers). For now, it's not established if Pyvelope will provide its own DI solution, use an existing one, or try to remain compatible with many DI containers like now. The only requirement is that MessageDispatcher is constructed with a ConsumerProvider that is able to provide Consumer instances when called.
