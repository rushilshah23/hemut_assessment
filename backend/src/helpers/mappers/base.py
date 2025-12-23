# src/helpers/mappers/base.py
from typing import List, TypeVar, Generic

ORM = TypeVar("ORM")
DTO = TypeVar("DTO")


class BaseMapper(Generic[ORM, DTO]):

    @staticmethod
    def to_dto(orm: ORM) -> DTO:
        raise NotImplementedError

    @staticmethod
    def to_orm(dto: DTO) -> ORM:
        raise NotImplementedError

    @classmethod
    def to_dto_list(cls, items: List[ORM]) -> List[DTO]:
        return [cls.to_dto(item) for item in items]

    @classmethod
    def to_orm_list(cls, items: List[DTO]) -> List[ORM]:
        return [cls.to_orm(item) for item in items]
