from urllib.parse import quote_plus as qp
from typing import Optional

from .scopes import Scopes


def generate_oauth_url(
    client_id: str,
    redirect_uri: str,
    *,
    state: Optional[str] = None,
    scopes: Optional[Scopes] = None,
    show_dialog: bool = False
) -> str:
    """A utility function to generate an OAuth URL with user-defined scopes and a redirect URI.

    Parameters
    ----------
    client_id: :class:`str`
        The Spotify client ID to authorize with.
    redirect_uri: :class:`str`
        The website to redirect to post-authorization with the code as a URL param. This **must**
        match the redirect URI on the Spotify dashboard.
    state: :class:`str`
        A string of ideally non-guessable characters to ensure an authentication request is the one
        you sent. This prevents against cross-site request forgery.
    scope: :class:`Scopes`
        The privileges to-be associated with the code returned by the OAuth request. If ``None``,
        authorization will be granted only to access publicly available information.
    show_dialog: :class:`bool`
        Whether or not to force the user to approve the app again if they've already done so.

    Returns
    -------
    :class:`str`
        The usable OAuth URL.
    """
    url = 'https://accounts.spotify.com/authorize?response_type=code' + \
          f'&client_id={client_id}' + \
          f'&redirect_uri={redirect_uri}'

    if state:
        url += f'&state={state}'
    if scopes:
        url_scopes = ' '.join(scope[0].replace('_', '-') for scope in scopes if scope[1])
        url += f'&scope={qp(url_scopes)}'
    if show_dialog:
        url += f'&show_dialog={str(show_dialog).lower()}'

    return url
