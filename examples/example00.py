bar = "bar"


def test_something():
    assert "foo"
    assert "..."
    assert True
    assert 0
    assert None
    assert "foo {0}".format(bar)
    assert f"foo {bar}"
