import datetime
from typing import TypedDict, Literal, Optional, Dict, List, Any
from typing_extensions import NotRequired

from .archetypes import SpotifyObject, SpotifyBasePayload
from .album import Album, AlbumPayload
from .artist import PartialArtist, PartialArtistPayload

__all__ = ('Track', )


class TrackExternalIDs(TypedDict):
    """Known external IDs for the track.

    Parameters
    -----------
    isrc: :class:`str`
        [International Standard Recording Code](http://en.wikipedia.org/wiki/International_Standard_Recording_Code)
    ean: :class:`str`
        [International Article Number](http://en.wikipedia.org/wiki/International_Article_Number_%28EAN%29)
    upc: :class:`str`
        [Universal Product Code](http://en.wikipedia.org/wiki/Universal_Product_Code)
    """
    isrc: NotRequired[str]
    ean: NotRequired[str]
    upc: NotRequired[str]


class TrackPayload(SpotifyBasePayload):
    album: AlbumPayload
    artists: List[PartialArtistPayload]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: bool
    external_ids: TrackExternalIDs
    external_urls: Dict[str, str]
    is_local: bool
    popularity: int
    preview_url: Optional[str]
    track_number: int


class Track(SpotifyObject):
    """Represents a track/song from Spotify.

    Attributes
    ----------
    name: :class:`str`
        The track's name.
    type: Literal['track']
        Will always be 'track'.
    uri: :class:`str`
        The Spotify URI of this track.
    id: :class:`str`
        The track's ID.
    album: :class:`Album`
        The track's album.
    artists: List[:class:`PartialArtist`]
        The track's artists.
    available_markets: List[:class:`str`]
        The markets that this track is available in.
    disc_number: :class:`int`
        The track's disc number.
    duration_ms: :class:`int`
        The track's duration.
    explicit: :class:`bool`
        Whether or not this track is explicit.
    external_ids: :class:`TrackExternalIDs`
        The track's external IDs.
    external_urls: Dict[:class:`str`, :class:`str`]
        The track's external URLs.
    is_playable: :class:`bool`
        Whether or not this track is playable in the given market.
    linked_from: Dict[:class:`Any`, :class:`Any`]
        Contains information about the originally requested track when Track Relinking is applied.
    restrictions: Optional[Dict[Literal['reason'], :class:`str`]]
        Included when a content restriction is applied; explains why it was applied.
    popularity: :class:`int`
        Represents the popularity of a track (0-100).
    preview_url: Optional[:class:`str`]
        Link to a 30 second preview (MP3).
    track_number: :class:`int`
        The track's number.
    is_local: :class:`bool`
        Whether or not the track is a local file.
    """
    album: Album
    artists: List[PartialArtist]
    available_markets: List[str]
    disc_number: int
    duration_ms: int
    explicit: Optional[bool]
    external_ids: TrackExternalIDs
    external_urls: Dict[str, str]
    is_playable: Optional[bool]
    linked_from: Optional[Dict[Any, Any]]
    restrictions: Optional[Dict[Literal['reason'], str]]
    popularity: int
    preview_url: Optional[str]
    track_number: int
    is_local: bool

    def __init__(
        self,
        data: TrackPayload
    ) -> None:
        super().__init__(data)

        # formatting the track's artists
        artists = [PartialArtist(i) for i in data['artists']]

        self.album: Album = Album(data['album'])
        self.artists: list[PartialArtist] = artists
        self.available_markets: list[str] = data['available_markets']
        self.disc_number: int = data['disc_number']
        self.duration: datetime.timedelta = datetime.timedelta(seconds=data['duration_ms'] / 1000)
        self.explicit: Optional[bool] = data['explicit']
        self.external_ids: TrackExternalIDs = data['external_ids']
        self.external_urls: dict[str, str] = data['external_urls']
        self.is_playable: Optional[bool] = data.get('is_playable')
        self.linked_from: Optional[Dict[Any, Any]] = data.get('linked_from')
        self.restrictions: Optional[Dict[Literal['reason'], str]] = data.get('restrictions')
        self.popularity: int = data['popularity']
        self.preview_url: Optional[str] = data['preview_url']
        self.track_number: int = data['track_number']
        self.is_local: bool = data['is_local']

    def __str__(self) -> str:
        return self.name
