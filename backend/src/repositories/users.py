from src.db.models import UserORM, AdminORM, GuestORM, RoleORM
from .base import BaseRepository
from sqlalchemy.exc import IntegrityError
from src.exceptions.database import DuplicateResourceError
from src.helpers.enums.errors import DatabaseErrorCodes

class UserRepository(BaseRepository[UserORM]):
    model = UserORM
    



    
class GuestRepository(BaseRepository[GuestORM]):
    model = GuestORM
    


class AdminRepository(BaseRepository[AdminORM]):
    model = AdminORM
    async def create_one(self, data):
        try:
            return await super().create_one(data)
        except IntegrityError as e:
            await self.session.rollback()

            orig = e.orig
            if hasattr(orig, "sqlstate") and orig.sqlstate == DatabaseErrorCodes.UNIQUE_VIOLATION.value:
                if "email" in str(orig):
                    raise DuplicateResourceError(f"email - {data.get('email')} already exists")

            raise


class RoleRepository(BaseRepository[RoleORM]):
    model = RoleORM