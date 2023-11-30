from chalicelib.extern.dependency_injector.persistant import PersistentInjector
from chalicelib.persistant.asyncio.command_factory import AsyncCommandFactory
from chalicelib.persistant.asyncio.invoker import AsyncInvoker


def test_persistent_injector_without_dependency(client):
    # given
    injector = PersistentInjector()
    # when & then
    try:
        injector.check_dependencies()
    except Exception:
        assert True
    else:
        assert False


def test_persistent_injector(client):
    # given
    injector = PersistentInjector(client=client)
    # when & then
    assert isinstance(injector.command_factory(), AsyncCommandFactory)
    assert isinstance(injector.invoker(), AsyncInvoker)
    assert injector.command_factory() is injector.command_factory()
    assert injector.invoker() is not injector.invoker()
