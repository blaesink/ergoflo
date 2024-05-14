from ergoflo.flow import checked
from ergoflo import Maybe, Nothing


class MyClass[T]:
    def __init__(self, value: Maybe[T] = Nothing()):
        self.val = value

    @checked
    def get_value(self) -> Maybe[T]:
        return self.val


def test_checked_functions():
    mc = MyClass()

    try:
        val = mc.get_value()
    except Exception:
        val = 3

    assert val == 3
