from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, TypedDict, Optional, Dict, List, Any

from yarl import URL

from .archetypes import SpotifyObject, SpotifyBasePayload, FollowerData
from .image import Image, ImagePayload
from .track import Track, TrackPayload
from .user import PartialUser, PartialUserPayload
from ..utils import Route

if TYPE_CHECKING:
    from ..http import HTTPClient


__all__ = ('Playlist', 'PlaylistTracks', 'PlaylistItem')


class NextTracksPayload(TypedDict):
    href: str
    items: List[PlaylistItemPayload]
    limit: int
    next: Optional[str]
    previous: Optional[str]
    offset: int
    total: int


class PlaylistItemPayload(TypedDict):
    added_at: str
    added_by: PartialUserPayload
    is_local: bool
    primary_color: Optional[int]
    track: TrackPayload
    video_thumbnail: Dict[str, str]


class PlaylistTracksPayload(TypedDict):
    """Not to be confused with a TrackPayload"""
    href: str
    items: List[PlaylistItemPayload]
    limit: int
    next: Optional[str]
    offset: int
    previous: Optional[str]
    total: int


class PlaylistItem:
    """Information about an item in a playlist.

    Attributes
    ----------
    added_at: :class:`datetime.datetime`
        The time at which the item as added.
    added_by: :class:`PartialUser`
        The user that added the item.
    is_local: :class:`bool`
        Whether or not the item is a local file.
    primary_color: Optional[:class:`int`]
        The primary color.
    track: :class:`Track`
        The track.
    video_thumbnail: Dict[:class:`str`, :class:`str`]
        The video thumbnail.
    """

    def __init__(self, data: PlaylistItemPayload):
        self.added_at: datetime.datetime = datetime.datetime.strptime(data['added_at'].split('T')[0], '%Y-%m-%d')
        self.added_by: PartialUser = PartialUser(data['added_by'])
        self.is_local: bool = data['is_local']
        self.primary_color: Optional[int] = data['primary_color']
        self.track: Track = Track(data['track'])
        self.video_thumbnail: Dict[str, str] = data['video_thumbnail']

    def __str__(self) -> str:
        return self.track.name

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"


class PlaylistTracks:
    """A list of the playlist's tracks.

    Attributes
    ----------
    items: List[:class:`PlaylistItem`]
        A list of items in the playlist.
    limit: :class:`int`
        Maximum number of items in the response.
    offset: :class:`int`
        Offset of the items returned.
    total: :class:`int`
        The total number of items available to return.
    """

    def __init__(self, data: PlaylistTracksPayload):
        # formatting the items
        items = [PlaylistItem(i) for i in data['items']]

        self._href: str = data['href']
        self.items: List[PlaylistItem] = items
        self.limit: int = data['limit']
        self._next: Optional[str] = data['next']
        self.offset: int = data['offset']
        self._previous: Optional[str] = data['previous']
        self.total: int = data['total']

    def __contains__(self, item: Any) -> bool:
        if not isinstance(item, Track):
            return False

        return any(item.id == i.track.id for i in self.items)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"


class PlaylistPayload(SpotifyBasePayload):
    collaborative: bool
    description: bool
    external_urls: Dict[str, str]
    followers: FollowerData
    images: List[ImagePayload]
    owner: Any
    primary_color: Optional[int]
    public: bool
    snapshot_id: str
    tracks: PlaylistTracksPayload


class Playlist(SpotifyObject):
    """Represents a playlist from Spotify

    Attributes
    ----------
    collaborative: :class:`bool`
        Whether or not the playlist is made by one or more people.
    description: :class:`bool`
        The playlist's description.
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs of this playlist.
    followers: :class:`FollowerData`
        The playlist's followers.
    images: List[:class:`Image`]
        The playlist's images.
    owner: :class:`PartialUser`
        The playlist's owner.
    public: :class:`bool`
        Whether or not the playlist is public.
    snapshot_id: :class:`str`
        The playlist's version identifier.
    tracks: :class:`PlaylistTracks`
        The playlist's tracks.
    """

    def __init__(self, data: PlaylistPayload, http: HTTPClient):
        super().__init__(data)

        # formatting the images
        images = [Image(i) for i in data['images']]

        self.collaborative: bool = data['collaborative']
        self.description: bool = data['description']
        self.external_urls: Dict[str, str] = data['external_urls']
        self.followers: FollowerData = data['followers']
        self.images: List[Image] = images
        self.owner: Any = data['owner']
        self.public: bool = data['public']
        self.snapshot_id: str = data['snapshot_id']
        self.tracks: PlaylistTracks = PlaylistTracks(data['tracks'])
        self._http: HTTPClient = http

    async def fetch_tracks(self) -> None:
        """|coro|
        A method to populate the playlist's tracks if it contains over 100 tracks.
        """
        next_ = self.tracks._next # type: ignore

        while next_ is not None:
            # not really ideal and defeats the purpose of Route
            # however i'm too lazy to make this "proper"
            route = Route('GET', '')
            route.url = URL(next_)

            res: NextTracksPayload = await self._http.request(route)
            self.tracks.items += [PlaylistItem(i) for i in res['items']]

            if self.tracks.offset + self.tracks.limit >= self.tracks.total:
                return

            next_ = res['next']
