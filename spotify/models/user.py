from typing import Literal, TypedDict, Dict, List, Any
from typing_extensions import NotRequired

from .archetypes import SpotifyObject, FollowerData
from .image import Image, ImagePayload

__all__ = ('User', 'PartialUser', )


# Can't use the base payload since there's no guaranteed name
class PartialUserPayload(TypedDict):
    display_name: NotRequired[str]
    href: str
    id: str
    type: Literal['user']
    uri: str
    external_urls: Dict[str, str]


class UserPayload(PartialUserPayload):
    country: str
    email: str
    explicit_content: Dict[str, Any]
    followers: FollowerData
    images: List[ImagePayload]
    product: str


class PartialUser(SpotifyObject):
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


class User(PartialUser):
    """Represents a Spotify user.

    Attributes
    ----------
    country: :class:`str`
        The user's country
    display_name: Optional[:class:`str`]
        The user's display name.
    email: :class:`str`
        The user's registered email
    explicit_content: Dict[:class:`str`, Any]
        Information regarding the user's explicit content filters
    external_urls: Dict[:class:`str`, :class:`str`]
        Known external URLs for the user.
    followers: :class:`FollowerData`
        The user's follower statistics
    href: :class:`str`
        ???
    id: :class:`str`
        The user's ID.
    images: List[:class:`Image`]
        The user's profile picture
    product: :class:`str`
        ???
    type: :class:`str`
        Will always be ``user``.
    uri: :class:`str`
        The Spotify URI for the user.
    """

    def __init__(self, data: UserPayload):
        super().__init__(data)
        self.country = data['country']
        self.email = data['email']
        self.explicit_content = data['explicit_content']
        self.followers = data['followers']
        self.images: List[Image] = [Image(i) for i in data['images']]
        self.product = data['product']
