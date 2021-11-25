# flake8-useless-assert
flake8 plugin to catch useless `assert` statements

Download or install on the [PyPI page](https://pypi.org/project/flake8-useless-assert/)

# Violations

| Code    | Description                                          |   Example                        |
|---------|------------------------------------------------------|----------------------------------|
| ULA001  | `assert` with a truthy literal                       | `assert "foo"`                   |
|         |                                                      | `assert ...`                     |
|         |                                                      | `assert True`                    |
| ULA002  | `assert` with `0`                                    | `assert 0`                       |
| ULA003  | `assert` with `None`                                 | `assert None`                    |
| ULA004  | `assert` with "literal".format(...)                  | `assert "foo {0}".format(bar)`   |
| ULA005  | `assert` with f-string                               | `assert f"foo {bar}"`            |
| ULA006  | `assert` with constant computation                   | `assert "foo" == "bar" * 3`      |


# Testing
I haven't set up proper testing yet, but you can run `poetry install` and then:
```
flake8 examples/
```