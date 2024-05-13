import pytest

from ergoflo import Err, Maybe, Ok, Result, Some, Nothing
from ergoflo.flow import checked, flow


def _add_two(x: int) -> int:
    return x + 2


def _fail_func(_: int) -> Result[int]:
    return Err(RuntimeError("oops"))


def test_simple_flow():
    assert flow(_add_two, _add_two)(0) == 4


def test_fallible_flow():
    assert flow(_add_two, _fail_func)(3) == Err(RuntimeError("oops"))
    assert flow(_add_two, lambda i: Ok(i))(3) == Ok(5)


def test_checked_func():
    def foo() -> Result[int]:
        return Err(ValueError("oops"))

    @checked
    def bar() -> Maybe[int]:
        return Some(foo().unwrap())

    with pytest.raises(ValueError):
        bar()


def test_check_func_ok():
    @checked
    def foo() -> Maybe[int]:
        return Some(3)

    @checked
    def bar() -> Result[int]:
        return Ok(foo().unwrap())

    assert bar() == Ok(3)


@pytest.mark.parametrize(
    "input",
    [
        Nothing(),
        Err(RuntimeError(0)),
    ],
)
def test_checked_bad(input):
    @checked
    def foo():
        return input

    with pytest.raises(RuntimeError):
        foo()
