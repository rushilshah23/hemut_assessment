from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.enums.user import RoleEnum
from src.helpers.dtos.users import UserDTO, AdminDTO


from src.helpers.mappers.users import UserMapper
from src.helpers.mappers.role import RoleMapper
from src.helpers.mappers.admin import AdminMapper


from src.repositories.users import RoleRepository, UserRepository, AdminRepository
from src.utils.misc import generate_uuid
from src.helpers.schemas.users import CreateAdmin, CreateAdminResponse


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.role_repo = RoleRepository(session)
        self.user_repo = UserRepository(session)
        self.admin_repo = AdminRepository(session)

    async def create_admin_user(self, create_admin: CreateAdmin):
        try:
            role_orm = await self.role_repo.get_one(
                name=RoleEnum.ADMIN.value
            )

            if not role_orm:
                raise ValueError("Admin role not found")

            user_id = generate_uuid()

            await self.user_repo.create_one({
                "id": user_id,
                "role_id": role_orm.id,
            })

            admin_orm = await self.admin_repo.create_one({
                "id": generate_uuid(),
                "user_id": user_id,
                "email": create_admin.email,
                "password": create_admin.password,
            })

            await self.session.commit()
            admin_dto =  AdminMapper.to_dto(admin_orm)
            create_admin_reponse = CreateAdminResponse(email=admin_dto.email,user_id=admin_dto.user_id, id=admin_dto.id)
            return create_admin_reponse

        except Exception:
            await self.session.rollback()
            raise
