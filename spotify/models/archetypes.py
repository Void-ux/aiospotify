from typing import TypedDict


class SpotifyBasePayload(TypedDict):
    href: str
    id: str
    name: str
    type: str
    uri: str


class SpotifyObject:
    _href: str
    id: str
    name: str
    type: str
    uri: str

    """An object from Spotify.

    Attributes
    ----------
    _href: :class:`str`
        A link to the web API endpoint for this object.
    id: :class:`str`
        The object's ID.
    name: :class:`str`
        The object's name.
    type: :class:`str`
        The type of the object.
    uri: :class:`str`
        The Spotify URI for this object.
    """
    def __init__(self, data: SpotifyBasePayload) -> None:
        self._href: str = data["href"]
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: str = data["type"]
        self.uri: str = data["uri"]

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"


class FollowerData(TypedDict):
    """Information about the followers of the item.

    Parameters
    -----------
    href: `None`
        This will always be set to null, as the Web API does not support it at the moment.
    total: :class:`int`
        The total number of followers.
    """
    href: None  # will be str when the API supports it
    total: int
