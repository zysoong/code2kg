from base.models import BaseGraphNodeModel
from models.oop import OOPModule, OOPFunction
from models.oop import OOPClass


def test_oop_function_within_class_constructor():
    qualified_name: str = "dummy_module.dummy_package.DummyClass.dummy_function"
    signature: str = "dummy_function(self, dummy_parameter)"
    code: str = "def dummy_function(self, dummy_parameter):\n\tdummy_var = dummy_parameter"
    flat_function_calls: list[OOPFunction] = []
    within: OOPClass = OOPClass(
        qualified_name="dummy_module.dummy_package.DummyClass",
        name="DummyClass",
        code="class DummyClass:\n"
             "\tdef __init__(self):\n\t\tself.dummy = 'dummy'\n"
             "\tdef dummy_function(self, dummy_parameter):\n\t\tdummy_var = dummy_parameter",
        super_classes=[],
        within=OOPModule(qualified_name="dummy_module.dummy_package")
    )

    oop_function = OOPFunction(
        qualified_name=qualified_name,
        signature=signature,
        code=code,
        flat_function_calls=flat_function_calls,
        within=within
    )

    assert oop_function.qualified_name == qualified_name
    assert oop_function.signature == signature
    assert oop_function.code == code
    assert oop_function.summary == ""

    assert oop_function.flat_function_calls == flat_function_calls
    assert oop_function.within == within

    assert oop_function.id == qualified_name
    assert oop_function.attributes == {
        "signature": signature,
        "code": code,
    }
    assert oop_function.relations == {
        "flat_function_calls": flat_function_calls,
        "within": within
    }


def test_oop_function_with_flat_calls_within_class_constructor():
    qualified_name: str = "dummy_module.dummy_package.DummyClass.dummy_function"
    signature: str = "dummy_function(self, dummy_parameter)"
    code: str = "def dummy_function(self, dummy_parameter):\n\tdummy_var = another_dummy_function(dummy_parameter)"

    called_function: OOPFunction = OOPFunction(
        qualified_name="dummy_utils.another_dummy_function",
        signature="another_dummy_function(dummy_parameter)",
        code="def another_dummy_function(self, dummy_parameter):\n\tprint(f'Hi, {dummy_parameter}')",
        flat_function_calls=[],
        within=OOPModule(qualified_name="dummy_utils")
    )
    flat_function_calls: list[OOPFunction] = [called_function]

    within: OOPClass = OOPClass(
        qualified_name="dummy_module.dummy_package.DummyClass",
        name="DummyClass",
        code="from dummy_utils import another_dummy_function"
             "class DummyClass:\n"
             "\tdef __init__(self):\n\t\tself.dummy = 'dummy'\n"
             "\tdef dummy_function(self, dummy_parameter):\n\t\tdummy_var = another_dummy_function(dummy_parameter)",
        super_classes=[],
        within=OOPModule(qualified_name="dummy_module.dummy_package")
    )

    oop_function = OOPFunction(
        qualified_name=qualified_name,
        signature=signature,
        code=code,
        flat_function_calls=flat_function_calls,
        within=within
    )

    assert oop_function.qualified_name == qualified_name
    assert oop_function.signature == signature
    assert oop_function.code == code
    assert oop_function.summary == ""

    assert oop_function.flat_function_calls == flat_function_calls
    assert oop_function.within == within

    assert oop_function.id == qualified_name
    assert oop_function.attributes == {
        "signature": signature,
        "code": code,
    }
    assert oop_function.relations == {
        "flat_function_calls": flat_function_calls,
        "within": within
    }
