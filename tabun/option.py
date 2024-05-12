"""
Instead of a function that returns, T | None, wrap it in a `Some`.
This is so that when you want to railroad function execution, you can do it safely
and without having to do endless checks.
"""

from typing import Type, TypeVar, Self, Callable
import tabun.result as result

T = TypeVar("T")
U = TypeVar("U")


class Some[T]:
    def __init__(self, val: T):
        self.val = val

    def __eq__(self, other) -> bool:
        return self.val == other.val

    def __repr__(self) -> str:  # pragma: no cover
        return f"Some({self.val})"

    def map(self, val: T) -> "Some[T]":
        return Some(val)

    def unwrap(self) -> T:
        return self.val

    def map_or(self, _: T, f: Callable[..., U]) -> "Some[U]":
        return Some(f())

    def or_val(self, _: T) -> Self:
        return self

    def then(self, f: Callable[..., U]) -> "Some[U]":
        return Some(f(self.val))

    def filter(self, f: Callable[..., bool]) -> "Some[T] | Type[Nothing]":
        if f(self.val):
            return self
        return Nothing

    def ok_or(self, _) -> result.Ok[T]:
        return result.Ok(self.val)


class Nothing:
    def __repr__(self) -> str:  # pragma: no cover
        return "Nothing"

    @classmethod
    def unwrap(cls):
        raise RuntimeError("Attempted to unwrap null value")

    @classmethod
    def map(cls, _) -> Type[Self]:
        return cls

    @classmethod
    def map_or(cls, default: T, _: Callable[..., U]) -> Some[T]:
        return Some(default)

    @classmethod
    def or_val(cls, v: T) -> Some[T]:
        return Some(v)

    @classmethod
    def then(cls, _: Callable[..., T]) -> Type[Self]:
        return cls

    @classmethod
    def filter(cls, _: Callable[..., bool]) -> Type[Self]:
        return cls

    @classmethod
    def ok_or(cls, err: Exception) -> result.Err:
        return result.Err(err)


Maybe = Some[T] | Nothing
