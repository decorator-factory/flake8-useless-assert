x = "string"


def ula006():
    assert "foo" == "bar"
    assert "foo" < "bar" != {"fizz": "buzz", **{"quack": ["duck"], "aaa": []}}
    assert "foo" < x < "bar"  # OK
    assert "foo" if True else "bar"
    assert "foo" + "bar"
    assert "hello" * (3 + 2)
    assert repr({"foo", "bar"}) != "43"
