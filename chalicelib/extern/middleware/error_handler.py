import logging
import traceback

from chalice.app import (
    ALL_ERRORS,
    ChaliceError,
    ChaliceUnhandledError,
    Request,
    Response,
)

from chalicelib.view.model.builder import ApiBuilder


logger = logging.getLogger("pyoniverse-api")


def handle_errors(event: Request, get_response):
    try:
        response: Response = get_response(event)
        if response.status_code != 200:
            for error in ALL_ERRORS:
                if error.STATUS_CODE == response.status_code:
                    raise error(response.body)
        if response.status_code == 500:
            raise ChaliceUnhandledError(response.body)
    except ChaliceUnhandledError as e:
        status_code = str(500)
        tb = traceback.format_exc()
        errors = str(tb)
        body = (
            ApiBuilder()
            .with_status_code(status_code)
            .with_status_message(errors)
            .build()
        )
        response = Response(body=body, status_code=500)
        logger.error(errors)
    except ChaliceError as e:
        status_code = str(e.STATUS_CODE)

        tb = traceback.format_exc()
        errors = str(tb)
        body = (
            ApiBuilder()
            .with_status_code(status_code)
            .with_status_message(errors)
            .build()
        )
        response = Response(body=body, status_code=e.STATUS_CODE)

        logger.error(errors)
    return response
