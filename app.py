def wsgi(environ, start_response):
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Hello World!"]


async def asgi(scope, receive, send):
    assert scope["type"] == "http"
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [(b"content-type", b"text/plain")],
        }
    )
    await send({"type": "http.response.body", "body": b"Hello World!"})
