import pytest

from chalicelib.entity.product import ProductEntity
from chalicelib.persistant.asyncio.mongo.command import (
    AsyncMongoEqualCommand,
    AsyncMongoSelectBySortByCommand,
    AsyncMongoSelectRandomCommand,
    AsyncMongoSortByLimit10Command,
)


def test_invalid_equal_command(client):
    # given
    rel_name = "error_rel_name"
    key, value = None, None
    # when & then
    with pytest.raises(AssertionError):
        AsyncMongoEqualCommand(
            client=client,
            rel_name=rel_name,
            key=key,
            value=value,
        )

        AsyncMongoEqualCommand(
            client=client,
            rel_name=None,
            key="key",
            value=value,
        )

        AsyncMongoEqualCommand(
            client=None,
            rel_name=rel_name,
            key="key",
            value=value,
        )


@pytest.mark.asyncio
async def test_equal_command(client):
    # given
    rel_name = "brands"
    db_name = "constant"
    key = "id"
    value = 1
    # when
    command = AsyncMongoSortByLimit10Command(
        rel_name=rel_name, db_name=db_name, key=key, value=value, client=client
    )
    result = await command.execute()
    # then
    assert len(result) <= 10
    assert sorted(result, key=lambda x: x.id) == result


@pytest.mark.asyncio
async def test_select_by_sort_by_command(client):
    # given
    command = AsyncMongoSelectBySortByCommand(
        client=client,
        rel_name="products",
        db_name="service",
        key="brands.id",
        value=1,
        sort_key="good_count",
        sort_value="desc",
        chunk_size=3,
    )
    # when
    result = await command.execute()
    # then
    assert len(result) <= 3
    assert sorted(result, key=lambda x: x.good_count, reverse=True) == result
    for r in result:
        p: ProductEntity = r
        ok = False
        for b in p.brands:
            if b.id == 1:
                ok = True
                break
        assert ok


@pytest.mark.asyncio
async def test_select_random_command(client):
    # given
    command = AsyncMongoSelectRandomCommand(
        client=client,
        rel_name="products",
        db_name="service",
        chunk_size=3,
    )
    # when
    r1 = await command.execute()
    r2 = await command.execute()
    r1 = set(e.id for e in r1)
    r2 = set(e.id for e in r2)
    # then
    assert r1 != r2
