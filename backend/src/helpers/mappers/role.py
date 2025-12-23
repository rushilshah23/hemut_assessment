# src/helpers/mappers/role_mapper.py
from src.db.models import RoleORM
from src.helpers.dtos import RoleDTO
from .base import BaseMapper


class RoleMapper(BaseMapper[RoleORM, RoleDTO]):

    @staticmethod
    def to_dto(role: RoleORM) -> RoleDTO:
        return RoleDTO(
            id=role.id,
            name=role.name,
        )

    @staticmethod
    def to_orm(dto: RoleDTO) -> RoleORM:
        return RoleORM(
            id=dto.id,
            name=dto.name,
        )
