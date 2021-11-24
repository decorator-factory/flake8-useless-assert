# flake8-useless-assert
flake8 plugin to catch useless `assert` statements


# Examples of what it will flag

```py
assert "string literal"
assert 0x2a
assert "call to {0}".format("format")
assert f"f-{str}ing"
assert True
assert ...
```


# Testing
I haven't set up proper testing yet, but you can run `poetry install` and then:
```
flake8 examples/
```