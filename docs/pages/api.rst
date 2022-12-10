.. currentmodule:: spotify

API Reference
=============
The following content outlines the API of aio-spotify.

.. note::
    This module uses the Python logging module to log diagnostic and error messages. If the logging module is not 
    configured, these logs will not be output anywhere.

Clients
-------

Client
~~~~~~
.. attributetable:: Client
.. autoclass:: Client()

Spotify Models
--------------

Models are classes that are received from Spotify, and are not intended to be created by users of the library.

.. danger::

    The classes listed below are **not intended to be created by users** and are also
    **read-only**.

    For example, this means that you should not make your own :class:`Track` instances
    nor should you modify the :class:`Track` instance yourself.

    If you want to get one of these model classes instances, they'd have to be through the API or a property of another
    object that had been fetched already.

Album
~~~~~
.. autoclass:: Album()

Artist
~~~~~~
.. autoclass:: Artist()

.. autoclass:: PartialArtist()

Image
~~~~~
.. autoclass:: Image()

Playback
~~~~~~~~
.. autoclass:: Activity()

Playlist
~~~~~~~~
.. autoclass:: Playlist()

Track
~~~~~
.. autoclass:: Track()

User
~~~~
.. autoclass:: PartialUser()