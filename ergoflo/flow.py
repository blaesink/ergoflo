"""
A `flow` is another name for a pipeline.
Its aim is to chain multiple functions together, called sequentially on a single input.
"""

from functools import reduce
from typing import Callable, Protocol

from ergoflo.option import Nothing, Some
from ergoflo.result import Err, Ok


class Unwrap[T](Protocol):
    def unwrap(self) -> T: ...


def flow[T](*funcs: Callable[..., T]) -> Callable[..., T]:
    """Aka \"compose\".
    `flow` chains multiple functions together, where the output of one is the input to another.

    You can also use `flow` as a "function builder". Since nothing is evaluated until called with an argument,
    `flow`s can be made by building up a sequence of functions, then just calling flow(*funcs) to create the object and
    then evaluated at a later time.

    `flow(f1, f2, f3)(x)` is the same as `f3(f2(f1(x)))`

    `flow` is useful for functions using `Maybe` and `Result` so that you can quickly make composable \
    pipelines so that they "railroad" expectedly.

    NOTE: `flow` is currently not ergonomic to use with `checked` functions and requires a lot of lambda functions.
          in order to keep the same "visual". Therefore, if you have `Result | Maybe` functions that can fail (via `checked`),
          it is best to currently keep them out of `flow`.
    """

    def curried(*input_values):
        # Apply each function in sequence to the input
        return reduce(lambda result, func: func(result), funcs, *input_values)

        # Get the return type of the last function in *funcs

    return curried


def checked[T](f: Callable[..., Unwrap[T]]) -> Callable:
    """Automatically handles error flow for fallible Result/Option types.

    Functions that are marked `@checked` handle error propogation automatically. But you *must* use them with
    other `@checked` functions for the full effect!

    Of note: a function that returns a `Result | Maybe` doesn't need to be marked `@checked` if you don't expect
    it to be used in a fallible way (e.g. you actually want to return the container).
    """

    def _checked(*args, **kwargs):
        try:
            result = f(*args, **kwargs)

            match result:
                case Ok() | Some():
                    return result
                case Err() | Nothing():
                    result.unwrap()
        except Exception as e:
            raise e

    return _checked
