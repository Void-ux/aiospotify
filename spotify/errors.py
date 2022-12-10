from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union, Dict, Any

if TYPE_CHECKING:
    from aiohttp import ClientResponse

__all__ = ('HTTPException', 'RateLimited', 'Unauthorized', 'Forbidden', 'NotFound', 'SpotifyServerError')


class SpotifyException(Exception):
    """Base exception class for spotify

    Ideally speaking, this could be caught to handle any exceptions raised from this library.
    """

    pass


class HTTPException(SpotifyException):
    """Exception that's raised when an HTTP request operation fails.

    Attributes
    ------------
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request. This is an
        instance of :class:`aiohttp.ClientResponse`.
    status: :class:`int`
        The code code of the HTTP request.
    text: :class:`str`
        The Spotify specific error code for the failure.
    """
    def __init__(self, response: ClientResponse, message: Optional[Union[Dict[str, Any], str]]):
        self.response: ClientResponse = response
        self.status: int = response.status
        self.text: str

        if isinstance(message, dict):
            self.text = message['error']['message']
        elif isinstance(message, str):
            self.text = message or ''

        fmt = '{0.status} {0.reason} '
        if len(self.text):
            fmt += ': {1}'

        super().__init__(fmt.format(self.response, self.text))


class RateLimited(SpotifyException):
    """Exception that's raised for when status code 429 occurs, and the
    ``retry_after`` exceeds the ``max_ratelimit_timeout``.

    Attributes
    ------------
    retry_after: :class:`float`
        The amount of seconds that the client should wait before retrying
        the request.
    """

    def __init__(self, retry_after: float, max_ratelimit_timeout: float):
        self.retry_after = retry_after
        super().__init__(
            'Too many requests. Retry-After exceeded configured max_ratelimit_timeout '
            f'({retry_after:.2f} > {max_ratelimit_timeout}).'
        )


class Unauthorized(HTTPException):
    """Exception that's raised for when status code 401 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class Forbidden(HTTPException):
    """Exception that's raised for when status code 403 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class NotFound(HTTPException):
    """Exception that's raised for when status code 404 occurs.

    Subclass of :exc:`HTTPException`
    """

    pass


class SpotifyServerError(Exception):
    """Exception that's raised for when a 500 range status code occurs.

    Subclass of :exc:`HTTPException`.
    """

    pass
