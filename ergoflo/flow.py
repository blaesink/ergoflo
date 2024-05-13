"""
A `flow` is another name for a pipeline.
Its aim is to chain multiple functions together, called sequentially on a single input.
"""

from typing import Callable
from functools import reduce


def flow[T](*funcs: Callable[..., T]) -> Callable[..., T]:
    """Aka \"compose\".
    `flow` chains multiple functions together, where the output of one is the input to another.

    You can also use `flow` as a "function builder". Since nothing is evaluated until called with an argument,
    `flow`s can be made by building up a sequence of functions, then just calling flow(*funcs) to create the object and
    then evaluated at a later time.

    `flow(f1, f2, f3)(x)` is the same as `f3(f2(f1(x)))`

    `flow` is useful for functions using `Maybe` and `Result` so that you can quickly make composable \
    pipelines so that they "railroad" expectedly.
    """

    def curried(input_value):
        # Apply each function in sequence to the input
        return reduce(lambda result, func: func(result), funcs, input_value)

        # Get the return type of the last function in *funcs

    return curried
