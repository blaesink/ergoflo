from contextlib import nullcontext
import pytest
from ergoflo.result import Ok, Err, Result


def test_ok_val():
    assert Ok(2).then(lambda x: x * 2) == Ok(4)


def test_err_val():
    assert Err(RuntimeError("foo")).then(lambda x: x * 2) == Err(RuntimeError("foo"))


@pytest.mark.parametrize(
    "input, expected",
    [(Ok(2), Ok("2")), (Err(RuntimeError("oops")), Err(RuntimeError("oops")))],
)
def test_map_result(input, expected):
    assert input.map(str) == expected


@pytest.mark.parametrize(
    "input, expected", [(Ok(2), Ok(2)), (Err(RuntimeError("oops")), Ok(4))]
)
def test_result_or(input, expected):
    assert input.or_(4) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        (Ok(Ok(2)), Ok(2)),
        (Ok(3), Ok(3)),
        (Ok(Err(RuntimeError("oops"))), Err(RuntimeError("oops"))),
        (Err(RuntimeError("Oops")), Err(RuntimeError("Oops"))),
    ],
)
def test_flatten(input, expected):
    assert input.flatten() == expected


@pytest.mark.parametrize(
    "input, raises",
    [
        (Err(RuntimeError("oops")), pytest.raises(RuntimeError)),
        (Ok(2), nullcontext()),
    ],
)
def test_unwrap(input, raises):
    with raises:
        input.unwrap()


def test_bigger_chain():
    class ParseIntError(Exception):
        pass

    def inner_func(x: str) -> Result[int]:
        try:
            return Ok(int(x))
        except Exception:
            return Err(ParseIntError())

    assert inner_func("a").then(lambda x: x * 2) == Err(ParseIntError())
