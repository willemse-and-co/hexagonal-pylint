import ast
from operator import mod
from re import M
import pytest
import pylint_hexagonal
import astroid
from astroid import nodes
from unittest.mock import patch
from pylint.testutils import CheckerTestCase, MessageTest


class TestHexagonalChecker(CheckerTestCase):
    CHECKER_CLASS = pylint_hexagonal.HexagonalChecker

    def test_core_imports_port(self):
        module = "example.core.application.service"
        code = """
        import example.core.port.serviceport as serviceport
        """
        node = astroid.extract_node(code, module)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_core_imports_from_port(self):
        module = "example.core.application.service"
        code = """
        from example.core.port.serviceport import ExampleServicePort #@
        from ..port.serviceport import ExampleDTO #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertNoMessages():
            self.checker.visit_importfrom(absolute)
            self.checker.visit_importfrom(relative)

    def test_core_imports_adapter(self):
        module = "example.core.application.service"
        code = """
        import example.adapters.api.api as api
        """
        node = astroid.extract_node(code, module)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="core-imports-adapters",
                node=node,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=38,
            )
        ):
            self.checker.visit_import(node)

    def test_core_imports_from_adapter(self):
        module = "example.core.application.service"
        code = """
        from example.adapters.api.api import API #@
        from ..adapters.api.api import API #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="core-imports-adapters",
                node=absolute,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=40,
            )
        ):
            self.checker.visit_importfrom(absolute)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="core-imports-adapters",
                node=relative,  # type: ignore
                line=3,
                col_offset=0,
                end_line=3,
                end_col_offset=34,
            )
        ):
            self.checker.visit_importfrom(relative)

    def test_adapter_imports_non_port_core(self):
        module = "example.adapters.db.connection"
        code = """
        import example.core.application.service as service
        """
        node = astroid.extract_node(code, module)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-core",
                node=node,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=50,
            )
        ):
            self.checker.visit_import(node)

    def test_adapter_imports_from_non_port_core(self):
        module = "example.adapters.db.connection"
        code = """
        from example.core.application.service import ExampleService #@
        from ...core.application.domain import ExampleAggregate #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-core",
                node=absolute,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=59,
            )
        ):
            self.checker.visit_importfrom(absolute)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-core",
                node=relative,  # type: ignore
                line=3,
                col_offset=0,
                end_line=3,
                end_col_offset=55,
            )
        ):
            self.checker.visit_importfrom(relative)

    def test_adapter_imports_port(self):
        module = "example.adapters.api.api"
        code = """
        import example.core.ports.serviceport as serviceport
        """
        node = astroid.extract_node(code, module)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_adapter_imports_from_port(self):
        module = "example.adapters.api.api"
        code = """
        from example.core.ports.serviceport import ExampleServicePort #@
        from ...core.ports.serviceport import ExampleDTO #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertNoMessages():
            self.checker.visit_importfrom(absolute)
            self.checker.visit_importfrom(relative)

    def test_adapter_imports_self(self):
        module = "example.adapters.api.api"
        code = """
        import example.adapters.api.serializers as serializers
        """
        node = astroid.extract_node(code, module)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_adapter_imports_from_self(self):
        module = "example.adapters.api.api"
        code = """
        from example.adapters.api.serializers import ExampleSerializer #@
        from .serializers import ExampleSerializer #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertNoMessages():
            self.checker.visit_importfrom(absolute)
            self.checker.visit_importfrom(relative)

    def test_adapter_imports_another_adapter(self):
        module = "example.adapters.api.api"
        code = """
        import example.adapters.db.connection as connection
        """
        node = astroid.extract_node(code, module)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-adapters",
                node=node,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=51,
            )
        ):
            self.checker.visit_import(node)


    def test_adapter_imports_from_another_adapter(self):
        module = "example.adapters.api.api"
        code = """
        from example.adapters.db.connection import Connection #@
        from ...adapters.db.connection import Connection #@
        """
        absolute, relative = astroid.extract_node(code, module)  # type: ignore
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-adapters",
                node=absolute,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=53,
            )
        ):
            self.checker.visit_importfrom(absolute)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="adapter-imports-adapters",
                node=relative,  # type: ignore
                line=3,
                col_offset=0,
                end_line=3,
                end_col_offset=48,
            )
        ):
            self.checker.visit_importfrom(relative)


    def test_port_includes_logic(self):
        module = "example.core.ports.serviceport"
        code = """
        def test(): #@
            print("test")

        class ExamplePort:
            def test(self): #@
                print("test")
        """
        func, method = astroid.extract_node(code, module)
        with self.assertAddsMessages(
            MessageTest(
                msg_id="port-includes-logic",
                node=func,  # type: ignore
                line=2,
                col_offset=0,
                end_line=2,
                end_col_offset=8,
            ),
            MessageTest(
                msg_id="port-includes-logic",
                node=method,  # type: ignore
                line=6,
                col_offset=4,
                end_line=6,
                end_col_offset=12,
            ),
        ):
            self.checker.visit_functiondef(func)
            self.checker.visit_functiondef(method)

    def test_port_does_not_include_logic(self):
        module = "example.core.ports.serviceport"
        code = """
        def test(self): #@
            pass
            
        class ExamplePort:
            def test(self): #@
                pass
        """
        func, method = astroid.extract_node(code, module) # type: ignore
        with self.assertNoMessages():
            self.checker.visit_functiondef(func)
            self.checker.visit_functiondef(method)


if __name__ == "__main__":
    pytest.main()
