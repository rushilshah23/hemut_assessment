from dataclasses import dataclass
from typing import Dict, Any



@dataclass(frozen=True)
class RoleDTO:
    id: int
    name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RoleDTO":
        return cls(
            id=int(data["id"]),
            name=data["name"],
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
        }

@dataclass(frozen=True)
class UserDTO:
    id: int
    role_id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserDTO":
        return cls(
            id=int(data["id"]),
            role_id=int(data["role_id"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "role_id": self.role_id,
        }


@dataclass(frozen=True)
class AdminDTO:
    id: int
    user_id: int
    email: str
    password:str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdminDTO":
        return cls(
            id=int(data["id"]),
            user_id=int(data["user_id"]),
            email=data["email"],
            password=data['password']
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
            "email": self.email,
            "password":self.password
        }


@dataclass(frozen=True)
class GuestDTO:
    id: int
    user_id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GuestDTO":
        return cls(
            id=int(data["id"]),
            user_id=int(data["user_id"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "user_id": self.user_id,
        }
