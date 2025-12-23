# from src.db.models import UserORM
# from src.db.models import RoleORM
# from src.db.models import AdminORM
# from src.db.models import GuestORM

# from src.helpers.dtos import UserDTO, RoleDTO, AdminDTO, GuestDTO


# # ---------- Role ----------

# def role_from_orm(role: RoleORM) -> RoleDTO:
#     return RoleDTO(
#         id=role.id,
#         name=role.name,
#     )


# # ---------- User ----------

# def user_from_orm(user: UserORM) -> UserDTO:
#     return UserDTO(
#         id=user.id,
#         role_id=user.role_id,
#     )


# # ---------- Admin ----------

# def admin_from_orm(admin: AdminORM) -> AdminDTO:
#     return AdminDTO(
#         id=admin.id,
#         user_id=admin.user_id,
#         email=admin.email,
#     )


# # ---------- Guest ----------

# def guest_from_orm(guest: GuestORM) -> GuestDTO:
#     return GuestDTO(
#         id=guest.id,
#         user_id=guest.user_id,
#     )


# def users_from_orm(users: list[UserORM]) -> list[UserORM]:
#     return [user_from_orm(u) for u in users]


# def roles_from_orm(roles: list[RoleORM]) -> list[RoleORM]:
#     return [role_from_orm(r) for r in roles]


# def admins_from_orm(admins: list[AdminORM]) -> list[AdminORM]:
#     return [admin_from_orm(a) for a in admins]


# def guests_from_orm(guests: list[GuestORM]) -> list[GuestORM]:
#     return [guest_from_orm(g) for g in guests]






# src/helpers/mappers/user_mapper.py
from src.db.models import UserORM
from src.helpers.dtos import UserDTO
from .base import BaseMapper


class UserMapper(BaseMapper[UserORM, UserDTO]):

    @staticmethod
    def to_dto(user: UserORM) -> UserDTO:
        return UserDTO(
            id=user.id,
            role_id=user.role_id,
        )

    @staticmethod
    def to_orm(dto: UserDTO) -> UserORM:
        return UserORM(
            id=dto.id,
            role_id=dto.role_id,
        )
