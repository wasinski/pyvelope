# Pyvelope

Pyvelope combines Python with the concept of an envelope: in ancient times, an envelope was a method for sending messages. Today, we have PubSub and similar technologies ;)

## The Problem

In the development of complex applications (modular monolith or microservices, anyone?), a very effective strategy for managing complexity and reducing latency in user-facing APIs is through the use of messaging, typically events. However, you cannot simply start dispatching these events to a queue within the transaction scope. If there's an issue with event delivery, it could cause the transaction to roll back. Likewise, sending the events after the transaction has been committed poses its own problems. If the events fail to reach the queue, it results in a system-wide inconsistency where the event was produced but not received by the consumers.

One solution, and perhaps the only option outside of Event Sourcing (correct me if I'm mistaken), is to employ the **Outbox Pattern**.

However, at the time of creating this repository, in the Python community, neither messaging communication nor the Outbox are well-known, established patterns. Let's change that!

## The Goals

This repository aims to:

- Demonstrate how the Outbox Pattern can be implemented in your system, serving as a model for straightforward replication (copy-cat).
- Offer a "plug-and-play" package for your application, enabling your app to facilitate message relay.
- Provide a standalone Relay Service.

The goals will be tackled in the order given. We'll see how far we get, what frameworks and platforms we can support for easy integration - time will tell. If you have any requests or suggestions, please raise an issue!
