# Pyvelope

Pyvelope combines Python with the concept of an envelope: in ancient times, an envelope was a method for sending messages. Today, we have PubSub, RequestReply and similar technologies ;)

## The Problem

In the development of complex applications (modular monolith or microservices, anyone?), a very effective strategy for managing complexity and reducing latency in user-facing APIs is through the use of messaging, typically events and commands. However, you cannot simply start dispatching these events to a queue within the transaction scope. If there's an issue with event delivery, it could cause the transaction to roll back. Likewise, sending the events after the transaction has been committed poses its own problems. If the events fail to reach the queue, it results in a system-wide inconsistency where the event was produced but not received by the consumers.

One solution, and perhaps the only option outside of Event Sourcing (correct me if I'm mistaken), is to employ the [**Outbox Pattern**](https://microservices.io/patterns/data/transactional-outbox.html).

However, at the time of creating this repository, in the Python community, neither messaging communication nor the Outbox are well-known, established patterns. Let's change that!

## The Goals

This repository aims to:

- Provide a MessageBus that supports both PubSub & RequestReply patterns
- Provide the Outbox Pattern support for your messages

We'll see what brokers, databases and platforms we can support for easy integration - time will tell. If you have any requests or suggestions, please raise an issue!

## Current progress

Basic APIs both for producer and consumer sides were established and can be looked up in `examples/`. For now the main focus will be to implement them for AWS cloud platforms, mainly SQS, Eventbridge and Lambda runtime.
