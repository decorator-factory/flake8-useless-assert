import ast
from typing import Callable, List, Optional, Sequence

from .flake_diagnostic import FlakeDiagnostic


class AssertTestVisitor(ast.NodeVisitor):
    def __init__(
        self,
        diagnostic_name: str,
        callback: Callable[[FlakeDiagnostic], None],
        detect_bad_assert_test: Callable[[ast.expr], Optional[str]],
    ):
        self._diagnostic_name = diagnostic_name
        self._callback = callback
        self._detect_bad_assert_test = detect_bad_assert_test

    def visit_Assert(self, node: ast.Assert) -> None:
        message = self._detect_bad_assert_test(node.test)

        if message is None:
            return

        diagnostic = FlakeDiagnostic(
            line=node.lineno,
            col=node.col_offset,
            message="{0} {1}".format(self._diagnostic_name, message),
        )
        self._callback(diagnostic)


Rule = Callable[[ast.Module], Sequence[FlakeDiagnostic]]


def _find_assert(
    diagnostic_name: str,
    detect_bad_assert_test: Callable[[ast.expr], Optional[str]]
) -> Rule:
    def _finder(module: ast.Module) -> Sequence[FlakeDiagnostic]:
        diagnostics: List[FlakeDiagnostic] = []
        visitor = AssertTestVisitor(
            diagnostic_name,
            diagnostics.append,
            detect_bad_assert_test,
        )
        visitor.visit(module)
        return diagnostics
    return _finder


def _detect_assert_test_with_truthy_literal(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.Constant):
        return None

    if not test.value:
        return None

    return "`assert` with a truthy value has no effect"


def _detect_assert_test_with_0(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.Constant):
        return None

    if test.value != 0:
        return None

    return "use `assert False` instead of `assert 0`"


def _detect_assert_test_with_none(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.Constant):
        return None

    if test.value is not None:
        return None

    return "use `assert False` instead of `assert None`"


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


def _detect_assert_test_with_fstring(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.JoinedStr):
        return None

    return "`assert` with an f-string"


def _detect_assert_test_with_format(test: ast.expr) -> Optional[str]:
    if not isinstance(test, ast.Call):
        return None

    if not _is_call_to_format(test):
        return None

    return "`assert` with 'literal'.format(...)"


rules: Sequence[Rule] = [
    _find_assert("ULA001", _detect_assert_test_with_truthy_literal),
    _find_assert("ULA002", _detect_assert_test_with_0),
    _find_assert("ULA003", _detect_assert_test_with_none),
    _find_assert("ULA004", _detect_assert_test_with_format),
    _find_assert("ULA005", _detect_assert_test_with_fstring),
]
