from models.oop import OOPModule


def test_oop_module_constructor():

    qualified_name: str = "dummy_module.dummy_package"

    oop_module = OOPModule(
        qualified_name=qualified_name
    )

    assert oop_module.qualified_name == qualified_name
    assert oop_module.id == qualified_name
    assert oop_module.attributes == {}
    assert oop_module.relations == {}
    