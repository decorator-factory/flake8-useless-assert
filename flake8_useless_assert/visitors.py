import ast
from typing import Callable, Optional

from .flake_diagnostic import FlakeDiagnostic


def _is_call_to_format(call: ast.Call) -> bool:
    """
    Check if a call is a call to `str.format`, like '{0}'.format(1).
    """
    if not isinstance(call.func, ast.Attribute):
        return False

    if not isinstance(call.func.value, ast.Constant):
        return False

    if not isinstance(call.func.value.value, str):
        return False

    return call.func.attr == "format"


def _detect_bad_assert_test_with_constant(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.Constant):
        return None

    if test.value is False:
        return None  # `assert False` is a valid idiom

    if test.value:
        return "`assert` with a truthy value has no effect"
    else:
        return "`assert` with a falsey value always fails. If you want this, do `assert False`"


def _detect_assert_test_with_formatted_string(test: ast.expr) -> Optional[str]:
    if isinstance(test, ast.JoinedStr):
        return "`assert` with an f-string has no effect"
    elif isinstance(test, ast.Call):
        if not _is_call_to_format(test):
            return
        return "`assert` with 'string'.format(...) has no effect"
    else:
        return None


class AssertWithConstantVisitor(ast.NodeVisitor):
    def __init__(self, callback: Callable[[FlakeDiagnostic], None]):
        self._callback = callback

    def visit_Assert(self, node: ast.Assert) -> None:
        message = _detect_bad_assert_test_with_constant(node.test)

        if message is None:
            return

        diagnostic = FlakeDiagnostic(
            line=node.lineno,
            col=node.col_offset,
            message="ULA001 {0}".format(message),
        )
        self._callback(diagnostic)


class AssertWithFormattedStrVisitor(ast.NodeVisitor):
    def __init__(self, callback: Callable[[FlakeDiagnostic], None]):
        self._callback = callback

    def visit_Assert(self, node: ast.Assert) -> None:
        message = _detect_assert_test_with_formatted_string(node.test)

        if message is None:
            return

        diagnostic = FlakeDiagnostic(
            line=node.lineno,
            col=node.col_offset,
            message="ULA002 {0}".format(message),
        )
        self._callback(diagnostic)
