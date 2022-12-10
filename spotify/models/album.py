import datetime
from enum import Enum
from typing import Literal, Dict, List

from .archetypes import SpotifyObject, SpotifyBasePayload
from .artist import PartialArtist, PartialArtistPayload
from .image import Image, ImagePayload

__all__ = ('Album', 'ReleaseDatePrecisions', 'AlbumType')


class ReleaseDatePrecisions(Enum):
    DAY = 'day'
    MONTH = 'month'
    YEAR = 'year'


class AlbumType(Enum):
    ALBUM = 'album'
    SINGLE = 'single'
    COMPILATION = 'compilation'


class AlbumPayload(SpotifyBasePayload):
    album_type: Literal['album', 'single', 'compilation']
    artists: List[PartialArtistPayload]
    available_markets: List[str]
    external_urls: Dict[str, str]
    images: List[ImagePayload]
    release_date: str
    release_date_precision: str
    total_tracks: int


class Album(SpotifyObject):
    """Represents an album from Spotify.

    Attributes
    ----------
    album_type: :class:`AlbumType`
        The album type; ``album``, ``single`` or ``compilation``.
    artists: List[:class:`PartialArtist`]
        The artists that made the album.
    available_markets: List[:class:`str`]
        The markets that the album is available in.
    external_urls: Dict[:class:`str`, :class:`str`]
        Any known external URLs for the album.
    href: :class:`str`
        A link to the web API endpoint for this album.
    id: :class:`str`
        The album's ID.
    images: List[:class:`Image`]
        Cover art for the album.
    name: :class:`str`
        The album's name.
    release_date: :class:`datetime.datetime`
        The release date of the album.
    release_date_precision: :class:`ReleaseDatePrecisions`
        The precision of the release date.
    total_tracks: :class:`int`
        The total number of tracks in the album.
    type: :class:`str`
        This will always be ``album``.
    uri: :class:`str`
        The Spotify URI for this album.
    """

    album_type: Literal['album', 'single', 'compilation']
    artists: List[PartialArtist]
    available_markets: List[str]
    external_urls: Dict[str, str]
    href: str
    id: str
    images: List[Image]
    name: str
    release_date: datetime.datetime
    release_date_precision: ReleaseDatePrecisions
    total_tracks: int
    type: str
    uri: str

    def __init__(self, data: AlbumPayload) -> None:
        super().__init__(data)

        # formatting the album's artists
        artists = [PartialArtist(i) for i in data['artists']]

        # converting the release date into a datetime.datetime
        release_date = datetime.datetime.strptime(
            data['release_date'],
            {
                ReleaseDatePrecisions.DAY.value: '%Y-%m-%d',
                ReleaseDatePrecisions.MONTH.value: '%Y-%m',
                ReleaseDatePrecisions.YEAR.value: '%Y'
            }[data['release_date_precision']]
        )

        # formatting the images
        images = [Image(i) for i in data['images']]

        self.album_type: Literal['album', 'single', 'compilation'] = data['album_type']
        self.artists: List[PartialArtist] = artists
        self.available_markets: List[str] = data['available_markets']
        self.external_urls: Dict[str, str] = data['external_urls']
        self.images: List[Image] = images
        self.release_date: datetime.datetime = release_date
        self.release_date_precision: ReleaseDatePrecisions = ReleaseDatePrecisions(data['release_date_precision'])
        self.total_tracks: int = data['total_tracks']

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<Album {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"
