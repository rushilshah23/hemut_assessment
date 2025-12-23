# src/helpers/mappers/guest_mapper.py
from src.db.models import GuestORM
from src.helpers.dtos import GuestDTO
from .base import BaseMapper


class GuestMapper(BaseMapper[GuestORM, GuestDTO]):

    @staticmethod
    def to_dto(guest: GuestORM) -> GuestDTO:
        return GuestDTO(
            id=guest.id,
            user_id=guest.user_id,
        )

    @staticmethod
    def to_orm(dto: GuestDTO) -> GuestORM:
        return GuestORM(
            id=dto.id,
            user_id=dto.user_id,
        )
