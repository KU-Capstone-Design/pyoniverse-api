import pytest
from chalice import BadRequestError

from chalicelib.entity.brand import BrandEntity
from chalicelib.service.brand.service import AsyncBrandService


@pytest.mark.asyncio
async def test_brand_service(factory, invoker):
    # given
    service = AsyncBrandService(command_factory=factory, invoker=invoker)
    # when & then
    with pytest.raises(BadRequestError):
        await service.find_by_slug(None)

    result = await service.find_by_slug(BrandEntity(slug="cu"))
    assert isinstance(result, BrandEntity)
