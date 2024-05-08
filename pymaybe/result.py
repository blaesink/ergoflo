"""
The `Result` type is used for functions that are *fallible*.

Meaning for example in cases that you would do a try/except and just raise
the error all the way up, you would instead catch it, wrap it in an `Err` and return
that to "railroad" the rest of the execution.
"""

from typing import TypeVar, Self, Callable

T = TypeVar("T")
U = TypeVar("U")


class Ok[T]:
    __match_args__ = ("v",)

    def __init__(self, val: T):
        self.val = val

    def __eq__(self, other) -> bool:
        return self.val == other.val

    def __repr__(self) -> str:  # pragma: no cover
        return f"Ok({self.val})"

    def then(self, f: Callable[..., U]) -> "Ok[U]":
        return Ok(f(self.val))

    def map(self, f: Callable[..., U]) -> "Ok[U]":
        return Ok(f(self.val))

    def or_(self, _: T) -> Self:
        return self

    def flatten(self) -> "Result[T]":
        match self.val:
            case Ok() | Err():
                return self.val
            case _:
                return self

    def unwrap(self) -> T:
        return self.val


class Err:
    __match_args__ = ("e",)

    def __init__(self, err: Exception):
        self._type = type(err)
        self.args = err.args

    def __eq__(self, other) -> bool:
        return self.args == other.args and self._type == other._type

    def __repr__(self) -> str:  # pragma: no cover
        return f"Err({self._type}({self.args}))"

    def then(self, _: Callable[..., U]) -> Self:
        return self

    def map(self, _: Callable[..., U]) -> Self:
        return self

    def or_(self, val: T) -> Ok[T]:
        return Ok(val)

    def flatten(self) -> Self:
        return self

    def unwrap(self) -> None:
        raise self._type(self.args)


Result = Ok[T] | Err
