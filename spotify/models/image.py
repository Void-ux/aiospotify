from typing import TypedDict

__all__ = ('Image', )


class ImagePayload(TypedDict):
    height: int
    width: int
    url: str


class Image:
    """Miscellaneous image corresponding to an existing Spotify object.

    Attributes
    ----------
    height: :class:`int`
        The image height in pixels.
    width: :class:`int`
        The image width in pixels.
    url: :class:`str`
        The source URL of the image.
    """
    def __init__(self, data: ImagePayload) -> None:
        self.height = data['url']
        self.width = data['height']
        self.url = data['url']

    def __str__(self) -> str:
        return self.url

    def __repr__(self) -> str:
        return f"<Image {' '.join(f'{attr}={value}' for attr, value in self.__dict__.items())}>"
