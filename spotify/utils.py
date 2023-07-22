from __future__ import annotations

import itertools
from typing import TYPE_CHECKING, Generator, Literal, Sequence, Tuple, Any
from urllib.parse import quote as _uriquote

from yarl import URL

if TYPE_CHECKING:
    from typing import TypeVar

    T = TypeVar('T')


# Credits to AbstractUmbra at https://github.com/AbstractUmbra/Hondana/blob/main/hondana/utils.py#L136-L160
# and to Danny at https://github.com/Rapptz/discord.py/blob/master/discord/http.py#L284-L319 for the initial implementation
class Route:
    """A helper class for instantiating a HTTP method to Spotify.

    Parameters
    -----------
    method: :class:`str`
        The HTTP method you wish to perform, e.g. ``"POST"``
    path: :class:`str`
        The prepended path to the API endpoint you with to target. e.g. ``"/me/player/currently-playing"``
    parameters: Any
        This is a special cased kwargs. Anything passed to these will substitute it's key to value in the `path`.
        E.g. if your `path` is ``"/me/player/currently-playing/{additional_types}"``, and your parameters are
        ``additional_types="..."``, then it will expand into the path making ``"/me/player/currently-playing/"``
    """

    BASE: str = 'https://api.spotify.com/v1'

    def __init__(self, method: Literal['GET', 'POST', 'PUT', 'DELETE'], path: str, **parameters: Any) -> None:
        self.method = method
        self.path = path
        url = self.BASE + self.path
        if parameters:
            url = url.format_map({k: _uriquote(v) if isinstance(v, str) else v for k, v in parameters.items()})

        self.url: URL = URL(url, encoded=True)


def grouper(n: int, iterable: Sequence[T]) -> Generator[Tuple[T, ...], Any, None]:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk
