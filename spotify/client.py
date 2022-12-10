from typing import Optional, Any
from typing_extensions import Self

import aiohttp

from .models.playback import Activity
from .models.track import Track
from .models.artist import Artist
from .models.playlist import Playlist

from .http import HTTPClient

__all__ = ('Client', )


class Client():
    """Represents a web client that sends requests to Spotify.
    This client is used to interact with Spotify's Web API.

    .. container:: operations
        .. describe:: async with x
            Asynchronously initialises the client and automatically cleans up.

    .. note::
        To be able to refresh tokens, the ``refresh_token``, ``client_id`` and ``client_secret`` must be provided.

    Parameters
    ----------
    access_token: :class:`str`
        The `Bearer` authorization token obtained from the authorization code/implicit grant flow.
    session: Optional[:class:`aiohttp.ClientSession`]
        The session to use, if not provided, one will be lazily created.
    refresh_token: Optional[:class:`str`]
        The refresh token to use upon the access token expiring. Spotify does not ever reset this.
    client_id: Optional[:class:`str`]
        The client ID to authenticate with upon refreshing a token.
    client_secret: Optional[:class:`str`]
        The client secret to authenticate with upon refreshing a token.
    """
    def __init__(
        self,
        access_token: str,
        session: Optional[aiohttp.ClientSession] = None,
        refresh_token: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None
    ) -> None:
        self.http = HTTPClient(access_token, session, refresh_token, client_id, client_secret)

    async def close(self):
        if self.http is not None:
            await self.http._close()  # type: ignore

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, exc_tb: Any):
        await self.close()

    # Artist

    async def fetch_artist(self, artist_id: str) -> Artist:
        """|coro|
        Fetches an artist using their ID.

        Parameters
        ----------
        artist_id: :class:`str`
            The artist's ID to fetch from.

        Returns
        -------
        :class:`Artist`
            The artist you requested.
        """
        data = await self.http.get_artist(artist_id)
        return Artist(data)

    # Track

    async def fetch_track(self, track_id: str) -> Track:
        """|coro|
        Fetches a track using its ID.

        Parameters
        ----------
        track_id: :class:`str`
            The tracks' ID to fetch from.

        Returns
        -------
        :class:`Track`
            The track you requested.
        """
        data = await self.http.get_track(track_id)
        return Track(data)

    # Playlist

    async def fetch_playlist(self, playlist_id: str) -> Playlist:
        """|coro|
        Fetches a playlist and its tracks using its ID.

        Parameters
        ----------
        playlist_id: :class:`str`
            The playlist's ID to fetch from.

        Returns
        -------
        :class:`Playlist`
            The playlist you requested.
        """
        data = await self.http.get_playlist(playlist_id)
        print(data)
        return Playlist(data)

    # Player

    async def fetch_currently_playing(self) -> Activity | None:
        """|coro|
        Fetches the currently playing item on a user's account.

        Returns
        -------
        Optional[:class:`Activity`]
            The current user's activity.

        .. note::
            This required the ``user_read_currently_playing`` scope.
        """
        data = await self.http.get_currently_playing()
        return Activity(data)
