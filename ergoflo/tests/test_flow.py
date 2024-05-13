from ergoflo.flow import flow
from ergoflo import Ok, Result, Err


def _add_two(x: int) -> int:
    return x + 2


def _fail_func(_: int) -> Result[int]:
    return Err(RuntimeError("oops"))


def test_simple_flow():
    assert flow(_add_two, _add_two)(0) == 4


def test_fallible_flow():
    assert flow(_add_two, _fail_func)(3) == Err(RuntimeError("oops"))
    assert flow(_add_two, lambda i: Ok(i))(3) == Ok(5)
