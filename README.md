# flake8-useless-assert
flake8 plugin to catch useless `assert` statements


# Violations

| Code    | Description                      |   Example                        |
|---------|----------------------------------|----------------------------------|
| ULA001  | `assert` with a literal          | `assert "foo"`                   |
|         |                                  | `assert ...`                     |
|         |                                  | `True`                           |
| ULA002  | `assert` with a formatted string | `assert "foo {0}".format(bar)`   |
|         |                                  | `assert f"foo {bar}"`            |

Note that `assert False` is exempt from `ULA001` because it's a common idiom.

# Testing
I haven't set up proper testing yet, but you can run `poetry install` and then:
```
flake8 examples/
```