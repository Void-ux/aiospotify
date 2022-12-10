from typing import Dict, List

from .archetypes import SpotifyObject, SpotifyBasePayload, FollowerData
from .image import Image, ImagePayload

__all__ = ('Artist', 'PartialArtist')


class PartialArtistPayload(SpotifyBasePayload):
    external_urls: Dict[str, str]


class PartialArtist(SpotifyObject):
    """Represents a "partial" Spotify artist.

    Attributes
    ----------
    href: :class:`str`
        A link to the web API endpoint for this artist.
    id: :class:`str`
        The artist's ID.
    type: :class:`str`
        The type of the artist.
    uri: :class:`str`
        The Spotify URI for this artist.
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs for this artist.
    """

    def __init__(self, data: PartialArtistPayload) -> None:
        super().__init__(data)
        self.external_urls: dict[str, str] = data['external_urls']

    def __repr__(self) -> str:
        return f"<PartialArtist {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"

    def __str__(self) -> str:
        return self.name


class ArtistPayload(SpotifyBasePayload):
    external_urls: Dict[str, str]
    followers: FollowerData
    genres: List[str]
    images: List[ImagePayload]
    popularity: int


class Artist(SpotifyObject):
    """Represents a Spotify artist.

    Attributes
    ----------
    href: :class:`str`
        A link to the web API endpoint for this artist.
    id: :class:`str`
        The artist's ID.
    type: :class:`str`
        The type of the artist.
    uri: :class:`str`
        The Spotify URI for this artist.
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs for this artist.
    images: List[:class:`Image`]
        Images of the artist.
    followers: :class:`FollowerData`
        Information about the artist's followers.
    genres: List[:class:`str`]
        Genres associated with the artist.
    popularity: :class:`int`
        Represents the popularity of an artist (0-100).
    """

    def __init__(self, data: ArtistPayload) -> None:
        super().__init__(data)
        self.external_urls: Dict[str, str] = data['external_urls']
        self.images: List[Image] = [Image(i) for i in data['images']]
        self.followers: FollowerData = data['followers']
        self.genres: List[str] = data['genres']
        self.popularity: int = data['popularity']

    def __repr__(self) -> str:
        return f"<Artist {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"

    def __str__(self) -> str:
        return self.name
