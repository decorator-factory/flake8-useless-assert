year = 2021


def get_bob_info():
    return {
        "name": "Bob",
        "copyright_sign": "(c) Bob 1976-{0}".format(year)
    }


def test_get_bob_info():
    bob_info = get_bob_info()
    assert bob_info["name"] == "Bob"
    assert f"(c) Bob 1976-{year}"
    assert "(c) Bob 1976-{0}".format(year)
    assert "test is done!"
    assert ...

    if False:
        assert 0

    if 0:
        assert False  # OK!
