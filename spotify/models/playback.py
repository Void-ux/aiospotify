import datetime
from enum import Enum
from typing import TypedDict, Optional, Literal, Dict, Any
from typing_extensions import NotRequired

from .track import Track, TrackPayload

__all__ = ('Activity', 'Context', 'PlayableTypes')


class PlayableTypes(Enum):
    TRACK = 'track'
    EPISODE = 'episode'
    AD = 'ad'


# TODO implement, however Spotify represents this weirdly
"""
class ActionsData(TypedDict):
    interrupting_playback: NotRequired[bool]
    pausing: NotRequired[bool]
    resuming: NotRequired[bool]
    seeking: NotRequired[bool]
    skipping_next: NotRequired[bool]
    skipping_prev: NotRequired[bool]
    toggling_repeat_context: NotRequired[bool]
    toggling_repeat_track: NotRequired[bool]
    toggling_shuffle: NotRequired[bool]
    transferring_playback: NotRequired[bool]


class Actions:
    def __init__(self, data: ActionsData) -> None:
        self.interrupting_playback: bool = data.get("interrupting_playback", False)
        self.pausing: bool = data.get("pausing", False)
        self.resuming: bool = data.get("resuming", False)
        self.seeking: bool = data.get("seeking", False)
        self.skipping_next: bool = data.get("skipping_next", False)
        self.skipping_previous: bool = data.get("skipping_prev", False)
        self.toggling_repeat_context: bool = data.get("toggling_repeat_context", False)
        self.toggling_repeat_track: bool = data.get("toggling_repeat_track", False)
        self.toggling_shuffle: bool = data.get("toggling_shuffle", False)
        self.transferring_playback: bool = data.get("transferring_playback", False)
"""


class ContextPayload(TypedDict):
    type: Literal['artist', 'playlist', 'album', 'show']
    href: str
    external_urls: Dict[str, str]
    uri: str


class Context:
    """Represents a Spotify context object.

    Attributes
    ----------
    type: :class:`str`
        Either ``artist``, ``playlist``, ``album`` or ``show``.
    href: :class:`str`
        A link to the web API endpoint for this context object.
    uri: :class:`str`
        The Spotify URI for this context object.
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs for this context object.
    """

    def __init__(self, data: ContextPayload) -> None:
        self.type = data['type']
        self.href = data['href']
        self.external_urls = data['external_urls']
        self.uri = data['uri']

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"


class DevicePayload(TypedDict):
    id: str
    is_active: bool
    is_private_session: bool
    is_restricted: bool
    name: str
    type: str
    volume_percent: int


class Device:
    def __init__(self, data: DevicePayload):
        self.id: str = data['id']
        self.is_active: bool = data['is_active']
        self.is_private_session: bool = data['is_private_session']
        self.is_restricted: bool = data['is_restricted']
        self.name: str = data['name']
        self.type: str = data['type']
        self.volume_percent: int = data['volume_percent']

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"


class ActivityPayload(TypedDict):
    device: NotRequired[DevicePayload]
    # repeat_state: str
    # shuffle_state: str
    context: ContextPayload
    timestamp: int
    progress_ms: int
    is_playing: bool
    item: TrackPayload
    currently_playing_type: Literal['track', 'episode', 'ad', 'unknown']
    actions: Any


class Activity:
    """Represents what the user is currently listening to.

    Attributes
    ----------
    device: Optional[:class:`Device`]
        The device on which the item is being played on.
    timestamp: :class:`datetime.datetime`
        The time the data was fetched by Spotify.
    context: Optional[:class:`Context`]
        The context object.
    progress: :class:`datetime.timedelta`
        The progress into the currently playing item.
    item: :class:`Track`
        The currently playing item, currently only tracks are supported.
    currently_playing_type: :class:`PlayableTypes`
        Either ``track``, ``episode``, ``ad`` or ``unknown``.
    actions: Dict[Any, Any]
        Which actions can be performed to the player based on the context.
    is_playing: Optional[:class:`bool`]
        Whether or not the item is playing or paused.
    """

    device: Optional[Device]
    timestamp: datetime.datetime
    context: Optional[Context]
    progress: datetime.timedelta
    item: Track
    currently_playing_type: PlayableTypes
    actions: Dict[Any, Any]
    is_playing: Optional[bool]

    def __init__(
        self,
        data: ActivityPayload
    ):
        # ensuring what's playing is either a track, episode or ad
        currently_playing_type = PlayableTypes(data['currently_playing_type'])

        if currently_playing_type != PlayableTypes.TRACK:
            raise NotImplementedError('Tracks are the only supported currently_playing_type')

        if data.get('device') is None:
            device = None
        else:
            device = Device(data['device'])  # type: ignore

        self.device: Optional[Device] = device
        self.timestamp: datetime.datetime = datetime.datetime.fromtimestamp(data['timestamp'] / 1000)
        self.context: Optional[Context] = Context(data['context'])
        self.progress: datetime.timedelta = datetime.timedelta(seconds=data['progress_ms'] / 1000)
        self.item: Track = Track(data['item'])
        self.currently_playing_type: PlayableTypes = currently_playing_type
        self.actions: Dict[Any, Any] = data['actions']
        self.is_playing: Optional[bool] = data['is_playing']

    def __str__(self) -> str:
        if len(self.item.artists) > 1:
            artists = ', '.join(artist.name for artist in self.item.artists[:-1])
            artists += f' and {self.item.artists[-1].name}'
        else:
            artists = self.item.artists[0].name

        return f'Listening to {self.item.name} by {artists}'

    def __repr__(self) -> str:
        return f"<Activity {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"
