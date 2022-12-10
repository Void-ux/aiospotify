from __future__ import annotations
import sys
import asyncio
import logging
import json
import base64
from typing import TYPE_CHECKING, TypeVar, Optional, Coroutine, Union, Any, Dict

import aiohttp

# from . import __version__
__version__ = '0.1.0a'
from .utils import Route
from .models.artist import ArtistPayload
from .models.playback import ActivityPayload
from .models.track import TrackPayload
from .models.playlist import PlaylistPayload
from .errors import (
    Unauthorized,
    Forbidden,
    NotFound,
    SpotifyServerError,
    RateLimited,
    HTTPException
)


if TYPE_CHECKING:
    T = TypeVar('T')
    Response = Coroutine[Any, Any, T]

__all__ = ('HTTPClient', )
LOGGER = logging.getLogger('spotify.http')


async def json_or_text(response: aiohttp.ClientResponse) -> Union[Dict[str, Any], str]:
    text = await response.text(encoding='utf-8')
    try:
        if response.headers['Content-Type'] in ('application/json', 'application/json; charset=utf-8'):
            return json.loads(text)
    except KeyError:
        # Thanks Cloudflare
        pass

    return text


class HTTPClient:
    """Represents a HTTP client sending HTTP requests to the Spotify API."""

    def __init__(
        self,
        access_token: str,
        session: Optional[aiohttp.ClientSession],
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        max_ratelimit_timeout: float = 30
    ) -> None:
        self.access_token = access_token
        self._refresh_token = refresh_token
        self._client_id = client_id
        self._client_secret = client_secret
        self._session = session
        self.max_ratelimit_timeout: float = max_ratelimit_timeout

        if any(i is not None for i in (self._refresh_token, self._client_id, self._client_secret)):
            assert all(i is not None for i in (refresh_token, client_id, client_secret)), \
                "When providing a refresh token, client id or a client secret, ensure all 3 are provided."

        user_agent = 'aio-spotify (https://github.com/Void-ux/aio-spotify {0}) Python/{0[0]}.{0[1]} aiohttp/{1}'
        self.user_agent: str = user_agent.format(__version__, sys.version_info, aiohttp.__version__)

    @staticmethod
    async def _generate_session() -> aiohttp.ClientSession:
        """|coro|

        Creates an :class:`aiohttp.ClientSession` for use in the http client.

        Returns
        --------
        :class:`aiohttp.ClientSession`
            The underlying client session we use.

        .. note::
            This method must be a coroutine to avoid the deprecation warning of Python 3.9+.
        """
        return aiohttp.ClientSession()

    async def _close(self) -> None:
        """|coro|

        This method will close the internal client session to ensure a clean exit.
        """

        if self._session is not None:
            await self._session.close()

    async def refresh_token(self) -> None:
        """|coro|

        This method will attempt to refresh the existing access token upon a status code of 401.
        """
        if self._session is None:
            self._session = await self._generate_session()

        data = {
            'grant_type': 'refresh_token',
            'refresh_token': self._refresh_token
        }
        client_authentication = base64.b64encode(f'{self._client_id}:{self._client_secret}'.encode('ascii'))
        headers = {
            'User-Agent': self.user_agent,
            'Authorization': f'Basic {client_authentication.decode("ascii")}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with self._session.post('https://accounts.spotify.com/api/token', data=data, headers=headers) as response:
            if not response.ok:
                response.raise_for_status()

            r = await response.json()
            self.access_token = r['access_token']

    async def request(self, route: Route, **kwargs: Any) -> Any:
        if self._session is None:
            self._session = await self._generate_session()

        headers: Dict[str, str] = {
            'User-Agent': self.user_agent,
            'Authorization': 'Bearer ' + self.access_token,
        }
        kwargs['headers'] = headers

        for tries in range(5):
            async with self._session.request(route.method, route.url, **kwargs) as response:
                data = await json_or_text(response)
                # print(dict(response.headers))
                # print(response)
                # print(response.content)

                if 300 > response.status >= 200:
                    return data

                # we are being rate limited
                if response.status == 429:
                    retry_after: float = float(response.headers['Retry-After'])
                    if retry_after > self.max_ratelimit_timeout:
                        raise RateLimited(retry_after, self.max_ratelimit_timeout)
                    fmt = 'We are being rate limited. %s %s responded with 429. Retrying in %.2f seconds.'
                    LOGGER.warning(fmt, response.method, response.url, retry_after)
                    await asyncio.sleep(retry_after)
                    continue

                # bad or expired token.
                if response.status == 401:
                    if self._refresh_token:
                        LOGGER.info('The access token has expired, attempting to refresh.')
                        try:
                            await self.refresh_token()
                        except Exception:
                            pass
                        else:
                            continue
                    raise Unauthorized(response, data)

                if response.status in {500, 502, 504, 524}:
                    await asyncio.sleep(1 + tries * 2)

                # re-authenticating won't help
                if response.status == 403:
                    raise Forbidden(response, data)
                elif response.status == 404:
                    raise NotFound(response, data)
                elif response.status >= 500:
                    raise SpotifyServerError(response, data)
                else:
                    raise HTTPException(response, data)

    def get_currently_playing(self) -> Response[ActivityPayload]:
        return self.request(Route('GET', '/me/player/currently-playing'))

    def get_playlist(self, playlist_id: str) -> Response[PlaylistPayload]:
        return self.request(Route('GET', '/playlists/{id}', id=playlist_id))

    def get_artist(self, artist_id: str) -> Response[ArtistPayload]:
        return self.request(Route('GET', '/artists/{id}', id=artist_id))

    def get_track(self, track_id: str) -> Response[TrackPayload]:
        return self.request(Route('GET', '/tracks/{id}', id=track_id))
