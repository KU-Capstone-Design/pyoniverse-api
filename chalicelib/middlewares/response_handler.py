import gzip

from chalice.app import ChaliceUnhandledError, Request, Response

from chalicelib.dtos.serializer import JsonSerializer


def handle_response(event: Request, get_response):
    print("Response Handler Enter")
    encoded_header = {
        "Content-Type": "application/json",
        "Content-Encoding": "gzip",
    }
    response: Response = get_response(event)
    response.headers.update(encoded_header)
    body: str = JsonSerializer.serialize(response.body)
    response.body = gzip.compress(body.encode("utf-8"))
    return response
