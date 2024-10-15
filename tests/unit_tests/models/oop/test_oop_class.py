from models.oop import OOPModule
from models.oop import OOPClass


def test_oop_class_constructor():

    qualified_name: str = "dummy_module.dummy_package.DummyClass"
    name: str = "DummyClass"
    code: str = "class DummyClass:\n\tdef __init__(self):\n\t\tself.dummy = 'dummy'"
    super_classes: list[OOPClass] = []
    within: list[OOPModule] = [OOPModule(qualified_name="dummy_module.dummy_package")]

    oop_class = OOPClass(
        qualified_name=qualified_name,
        name=name,
        code=code,
        super_classes=super_classes,
        within=within
    )

    assert oop_class.qualified_name == qualified_name
    assert oop_class.name == name
    assert oop_class.code == code
    assert oop_class.summary == ""

    assert oop_class.super_classes == super_classes
    assert oop_class.within == within

    assert oop_class.id == qualified_name
    assert oop_class.attributes == {
        "name": name,
        "code": code,
    }
    assert oop_class.relations == {
        "super_classes": super_classes,
        "within": within
    }



