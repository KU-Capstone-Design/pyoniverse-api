import pytest

from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.service.constant_brand.service import AsyncConstantBrandService


@pytest.mark.asyncio
async def test_constant_brand_service(factory, invoker):
    # given
    service = AsyncConstantBrandService(command_factory=factory, invoker=invoker)
    # when & then
    result = await service.find_all()
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(r, ConstantBrandEntity) for r in result)
