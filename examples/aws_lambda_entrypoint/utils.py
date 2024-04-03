def eventbridge_event_factory() -> dict[str, object]:
    return {
        "version": "0",
        "id": "6a7e8feb-b491-4cf7-a9f1-bf3703467718",
        "detail-type": "MyEvent",
        "source": "com.example.myapp",
        "account": "111122223333",
        "time": "2017-12-22T18:43:48Z",
        "region": "us-west-1",
        "resources": ["arn:aws:ec2:us-west-1:123456789012:instance/i-1234567890abcdef0"],
        "detail": {
            # and more...
            "type": "MyEvent",
            "correlation_id": "d734b3e3-5b0b-4c6c-9b69-2d0d3f3e3e3e",
            "message": {"body": "Hello, World!"},
            "sender": "com.example.myapp",
            "response_address": "https://sqs.us-east-1.amazonaws.com/123456789012/my_queue",
        },
    }
