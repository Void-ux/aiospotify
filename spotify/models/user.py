from typing import Literal, TypedDict, Dict
from typing_extensions import NotRequired

__all__ = ('PartialUser', )


class PartialUserPayload(TypedDict):
    display_name: NotRequired[str]
    href: str
    id: str
    type: Literal['user']
    uri: str
    external_urls: Dict[str, str]


class PartialUser:
    """Represents a "partial" Spotify user.

    Attributes
    ----------
    display_name: Optional[:class:`str`]
        The user's display name.
    id: :class:`str`
        The user's ID.
    type: :class:`str`
        Will always be ``user``.
    uri: :class:`str`
        The Spotify URI for the user.
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs for the user.
    """

    def __init__(self, data: PartialUserPayload):
        self.display_name = data.get('display_name')
        self._href: str = data["href"]
        self.id: str = data["id"]
        self.type: Literal['user'] = data["type"]
        self.uri: str = data["uri"]
        self.external_urls: Dict[str, str] = data['external_urls']
