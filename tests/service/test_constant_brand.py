from dataclasses import asdict

import pytest

from chalicelib.entity.constant_brand import ConstantBrandEntity
from chalicelib.service.constant_brand.service import AsyncConstantBrandService


@pytest.mark.asyncio
async def test_find_all(factory):
    # given
    service = AsyncConstantBrandService(factory=factory)
    # when & then
    result = await service.find_all()
    assert isinstance(result, list)
    assert len(result) > 0
    assert all(isinstance(r, ConstantBrandEntity) for r in result)
    for r in result:
        for v in asdict(r).values():
            assert v is not None


@pytest.mark.asyncio
async def test_find_slug(factory):
    service = AsyncConstantBrandService(factory=factory)
    result = await service.find_by_slug(ConstantBrandEntity(slug="cu"))
    assert isinstance(result, ConstantBrandEntity)
    assert result.slug == "cu"
    for v in asdict(result).values():
        assert v is not None
