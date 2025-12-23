# src/helpers/mappers/admin_mapper.py
from src.db.models import AdminORM
from src.helpers.dtos import AdminDTO
from .base import BaseMapper


class AdminMapper(BaseMapper[AdminORM, AdminDTO]):

    @staticmethod
    def to_dto(admin: AdminORM) -> AdminDTO:
        return AdminDTO(
            id=admin.id,
            user_id=admin.user_id,
            email=admin.email,
            password=admin.password
        )

    @staticmethod
    def to_orm(dto: AdminDTO) -> AdminORM:
        return AdminORM(
            id=dto.id,
            user_id=dto.user_id,
            email=dto.email,
            password=dto.password
        )
