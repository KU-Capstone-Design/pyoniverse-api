import traceback

from chalice.app import ChaliceError, ChaliceUnhandledError, Request, Response

from chalicelib.dtos.builder import ApiBuilder


def handle_errors(event: Request, get_response):
    try:
        response: Response = get_response(event)
        if response.status_code == 500:
            raise ChaliceUnhandledError()
    except ChaliceUnhandledError as e:
        status_code = str(500)
        status_message = None
        tb = traceback.format_exc()
        errors = str(tb).split("\n")
        body = (
            ApiBuilder()
            .with_status_code(status_code)
            .with_status_message(status_message)
            .with_errors(errors)
            .build()
        )
        response = Response(body=body, status_code=500)
    except ChaliceError as e:
        status_code = str(e.STATUS_CODE)
        status_message = None
        tb = traceback.format_exc()
        errors = str(tb).split("\n")
        body = (
            ApiBuilder()
            .with_status_code(status_code)
            .with_status_message(status_message)
            .with_errors(errors)
            .build()
        )
        response = Response(body=body, status_code=e.STATUS_CODE)
    return response
