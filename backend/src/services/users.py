from sqlalchemy.ext.asyncio import AsyncSession

from src.helpers.enums.user import RoleEnum
from src.helpers.dtos.users import UserDTO, AdminDTO


from src.helpers.mappers.users import UserMapper
from src.helpers.mappers.role import RoleMapper
from src.helpers.mappers.admin import AdminMapper


from src.repositories.users import RoleRepository, UserRepository, AdminRepository
from src.utils.misc import MiscUtils
from src.helpers.schemas.users import CreateAdmin, CreateAdminResponse


from src.validators.users import UserValidators


from src.exceptions.auth import InvalidCredentialsError
from src.helpers.schemas.users import LoginAdmin, LoginAdminResponse
from src.helpers.mappers.admin import AdminMapper
from src.utils.misc import MiscUtils



class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.role_repo = RoleRepository(session)
        self.user_repo = UserRepository(session)
        self.admin_repo = AdminRepository(session)

    async def create_admin_user(self, create_admin: CreateAdmin):
        try:

            UserValidators.Email.validate(create_admin.email)
            UserValidators.Password.validate(create_admin.password)
            UserValidators.PasswordEqualsConfirmPassword.validate(
                create_admin.password,
                create_admin.confirm_password
            )
            role_orm = await self.role_repo.get_one(
                name=RoleEnum.ADMIN.value
            )

            if not role_orm:
                raise ValueError("Admin role not found")

            user_id = MiscUtils.generate_uuid()

            await self.user_repo.create_one({
                "id": user_id,
                "role_id": role_orm.id,
            })

            hashed_password = MiscUtils.hash_password(password=create_admin.password)
            admin_orm = await self.admin_repo.create_one({
                "id": MiscUtils.generate_uuid(),
                "user_id": user_id,
                "email": create_admin.email,
                "password": hashed_password,
            })

            await self.session.commit()
            admin_dto =  AdminMapper.to_dto(admin_orm)
            create_admin_reponse = CreateAdminResponse(email=admin_dto.email,user_id=admin_dto.user_id, id=admin_dto.id)
            return create_admin_reponse

        except Exception:
            await self.session.rollback()
            raise





    async def login_admin(self, login_data: LoginAdmin) -> LoginAdminResponse:
        try:
            UserValidators.Email.validate(login_data.email)
            UserValidators.Password.validate(login_data.password)

            admin_orm = await self.admin_repo.get_one(
                email=login_data.email
            )

            if not admin_orm:
                raise InvalidCredentialsError()

            is_valid = MiscUtils.verify_password(
                password=login_data.password,
                hashed=admin_orm.password
            )

            if not is_valid:
                raise InvalidCredentialsError()

            admin_dto = AdminMapper.to_dto(admin_orm)

            return LoginAdminResponse(
                id=admin_dto.id,
                user_id=admin_dto.user_id,
                email=admin_dto.email,
                access_token="SAMPLE_TOKEN"
            )

        except Exception:
            await self.session.rollback()
            raise