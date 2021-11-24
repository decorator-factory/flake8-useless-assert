import ast
from typing import Iterator, List

from flake8_useless_assert.flake_diagnostic import FlakeDiagnostic
from flake8_useless_assert.useless_assert_visitor import UselessAssertVisitor

from .patch_const import LegacyConstantRewriter


class UselessAssert:
    name = "flake8-useless-assert"
    version = "0.1.3"

    def __init__(self, tree: ast.Module) -> None:
        self._tree = tree

    def __iter__(self) -> Iterator[FlakeDiagnostic]:
        LegacyConstantRewriter().visit(self._tree)

        diagnostics: List[FlakeDiagnostic] = []
        UselessAssertVisitor(diagnostics.append).visit(self._tree)

        yield from diagnostics
