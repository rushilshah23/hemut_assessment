from typing import Type, TypeVar, Generic, Iterable, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete





T = TypeVar("T")


class BaseRepository(Generic[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one(self, **filters) -> Optional[T]:
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_many_filtered(
        self,
        *,
        filters: dict | None = None,
        limit: int = 50,
        offset: int = 0,
        order_by=None,
    ) -> list[T]:
        stmt = select(self.model)

        if filters:
            stmt = stmt.filter_by(**filters)

        if order_by is not None:
            stmt = stmt.order_by(order_by)

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_one(self, data: dict) -> T:
        obj = self.model(**data)
        self.session.add(obj)
        await self.session.flush()
        return obj



    async def update_one(self, filters: dict, data: dict) -> Optional[T]:
        stmt = (
            update(self.model)
            .filter_by(**filters)
            .values(**data)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_one(self, **filters) -> bool:
        stmt = delete(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.rowcount > 0
