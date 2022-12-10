from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, ClassVar, Dict, Iterator, Optional, Tuple, Type, TypeVar, overload
from functools import reduce

from .enums import SpotifyScopes

if TYPE_CHECKING:
    from typing_extensions import Self

__all__ = ('Scopes', )
BF = TypeVar('BF', bound='BaseFlags')


class flag_value:
    def __init__(self, func: Callable[[Any], int]):
        self.flag: int = func(None)
        self.__doc__: Optional[str] = func.__doc__

    @overload
    def __get__(self, instance: None, owner: Type[BF]) -> Self:
        ...

    @overload
    def __get__(self, instance: BF, owner: Type[BF]) -> bool:
        ...

    def __get__(self, instance: Optional[BF], owner: Type[BF]) -> Any:
        if instance is None:
            return self
        return instance._has_flag(self.flag)  # type: ignore

    def __set__(self, instance: BaseFlags, value: bool) -> None:
        instance._set_flag(self.flag, value)  # type: ignore

    def __repr__(self) -> str:
        return f'<flag_value flag={self.flag!r}>'


def fill_with_flags(*, inverted: bool = False) -> Callable[[Type[BF]], Type[BF]]:
    def decorator(cls: Type[BF]) -> Type[BF]:
        # fmt: off
        cls.VALID_FLAGS = {
            name: value.flag
            for name, value in cls.__dict__.items()
            if isinstance(value, flag_value)
        }
        # fmt: on

        if inverted:
            max_bits = max(cls.VALID_FLAGS.values()).bit_length()
            cls.DEFAULT_VALUE = -1 + (2**max_bits)
        else:
            cls.DEFAULT_VALUE = 0

        return cls

    return decorator


class alias_flag_value(flag_value):
    pass


# n.b. flags must inherit from this and use the decorator above
class BaseFlags:
    VALID_FLAGS: ClassVar[Dict[str, int]]
    DEFAULT_VALUE: ClassVar[int]

    value: int

    __slots__ = ('value',)

    def __init__(self, **kwargs: bool):
        self.value = self.DEFAULT_VALUE
        for key, value in kwargs.items():
            if key not in self.VALID_FLAGS:
                raise TypeError(f'{key!r} is not a valid flag name.')
            setattr(self, key, value)

    @classmethod
    def _from_value(cls, value: Any):
        self = cls.__new__(cls)
        self.value = value
        return self

    def __or__(self, other: Self) -> Self:
        return self._from_value(self.value | other.value)

    def __and__(self, other: Self) -> Self:
        return self._from_value(self.value & other.value)

    def __xor__(self, other: Self) -> Self:
        return self._from_value(self.value ^ other.value)

    def __ior__(self, other: Self) -> Self:
        self.value |= other.value
        return self

    def __iand__(self, other: Self) -> Self:
        self.value &= other.value
        return self

    def __ixor__(self, other: Self) -> Self:
        self.value ^= other.value
        return self

    def __invert__(self) -> Self:
        max_bits = max(self.VALID_FLAGS.values()).bit_length()
        max_value = -1 + (2**max_bits)
        return self._from_value(self.value ^ max_value)

    def __bool__(self) -> bool:
        return self.value != self.DEFAULT_VALUE

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__) and self.value == other.value

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(self.value)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} value={self.value}>'

    def __iter__(self) -> Iterator[Tuple[str, bool]]:
        for name, value in self.__class__.__dict__.items():
            if isinstance(value, alias_flag_value):
                continue

            if isinstance(value, flag_value):
                yield (name, self._has_flag(value.flag))

    def _has_flag(self, o: int) -> bool:
        return (self.value & o) == o

    def _set_flag(self, o: int, toggle: bool) -> None:
        if toggle is True:
            self.value |= o
        elif toggle is False:
            self.value &= ~o
        else:
            raise TypeError(f'Value to set for {self.__class__.__name__} must be a bool.')


@fill_with_flags()
class Scopes(BaseFlags):

    __slots__ = ()

    @flag_value
    def ugc_image_upload(self):
        return SpotifyScopes.UGC_IMAGE_UPLOAD.value

    @flag_value
    def user_read_playback_state(self):
        return SpotifyScopes.USER_READ_PLAYBACK_STATE.value

    @flag_value
    def app_remote_control(self):
        return SpotifyScopes.APP_REMOTE_CONTROL.value

    @flag_value
    def user_modify_playback_state(self):
        return SpotifyScopes.USER_MODIFY_PLAYBACK_STATE.value

    @flag_value
    def playlist_read_private(self):
        return SpotifyScopes.PLAYLIST_READ_PRIVATE.value

    @flag_value
    def user_follow_modify(self):
        return SpotifyScopes.USER_FOLLOW_MODIFY.value

    @flag_value
    def playlist_read_collaborative(self):
        return SpotifyScopes.PLAYLIST_READ_COLLABORATIVE.value

    @flag_value
    def user_follow_read(self):
        return SpotifyScopes.USER_FOLLOW_READ.value

    @flag_value
    def user_read_currently_playing(self):
        return SpotifyScopes.USER_READ_CURRENTLY_PLAYING.value

    @flag_value
    def user_read_playback_position(self):
        return SpotifyScopes.USER_READ_PLAYBACK_POSITION.value

    @flag_value
    def user_library_modify(self):
        return SpotifyScopes.USER_LIBRARY_MODIFY.value

    @flag_value
    def playlist_modify_private(self):
        return SpotifyScopes.PLAYLIST_MODIFY_PRIVATE.value

    @flag_value
    def playlist_modify_public(self):
        return SpotifyScopes.PLAYLIST_MODIFY_PUBLIC.value

    @flag_value
    def user_read_email(self):
        return SpotifyScopes.USER_READ_EMAIL.value

    @flag_value
    def user_top_read(self):
        return SpotifyScopes.USER_TOP_READ.value

    @flag_value
    def streaming(self):
        return SpotifyScopes.STREAMING.value

    @flag_value
    def user_read_recently_played(self):
        return SpotifyScopes.USER_READ_RECENTLY_PLAYED.value

    @flag_value
    def user_read_private(self):
        return SpotifyScopes.USER_READ_PRIVATE.value

    @flag_value
    def user_library_read(self):
        return SpotifyScopes.USER_LIBRARY_READ.value

    @classmethod
    def all(cls) -> Self:
        value = reduce(lambda a, b: a | b, cls.VALID_FLAGS.values())
        self = cls.__new__(cls)
        self.value = value
        return self

    @classmethod
    def default(cls) -> Self:
        """Enables all the scopes required for reading values from the API."""
        self = cls.all()
        self.ugc_image_upload = False
        self.app_remote_control = False
        self.user_modify_playback_state = False
        self.user_follow_modify = False
        self.user_library_modify = False
        self.playlist_modify_private = False
        self.playlist_modify_public = False
        self.streaming = False
        return self
