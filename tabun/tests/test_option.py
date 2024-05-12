import pytest
from tabun.option import Some, Nothing
from tabun.result import Err, Ok


def test_get_some_val():
    assert Some(3).unwrap() == 3


def test_unwrap_nothing():
    with pytest.raises(RuntimeError):
        Nothing.unwrap()


@pytest.mark.parametrize(
    "input,map_val,expected", [(Some(3), 0, Some(0)), (Nothing, 0, Nothing)]
)
def test_map_option(input, map_val, expected):
    assert input.map(map_val) == expected


@pytest.mark.parametrize(
    "input,map_val,expected",
    [(Some(3), (1, lambda: 0), Some(0)), (Nothing, (2, lambda: 0), Some(2))],
)
def test_map_or_else_option(input, map_val, expected):
    assert input.map_or(*map_val) == expected


@pytest.mark.parametrize(
    "input,val,expected", [(Some(3), 0, Some(3)), (Nothing, 3, Some(3))]
)
def test_or_val_option(input, val, expected):
    assert input.or_val(val) == expected


def test_big_option_chain():
    x = Some(3).or_val(2).map(100)
    assert x == Some(100)


def test_big_option_chain_with_lambda():
    x = Some(3).or_val(100).map_or(3, lambda: "r")
    assert x == Some("r")


@pytest.mark.parametrize("input,expected", [(Some(3), Some(6)), (Nothing, Nothing)])
def test_option_then(input, expected):
    assert input.then(lambda x: x * 2).then(lambda x: x) == expected


@pytest.mark.parametrize(
    "input,expected", [(Some(4), Some(4)), (Some(3), Nothing), (Nothing, Nothing)]
)
def test_option_filter(input, expected):
    def is_even(x: int):
        return x % 2 == 0

    assert input.filter(is_even) == expected


@pytest.mark.parametrize(
    "input,expected",
    [(Some(2), Ok(2)), (Nothing, Err(RuntimeError("oops")))],
)
def test_option_ok_or(input, expected):
    assert input.ok_or(RuntimeError("oops")) == expected
