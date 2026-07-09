from dataclasses import dataclass


@dataclass
class LoginDTO:
    email: str
    password: str


@dataclass
class RegisterDTO:
    email: str
    password: str
    full_name: str
    community_id: int
    phone: str | None = None


@dataclass
class AdminRegisterDTO:
    email: str
    password: str
    full_name: str
    community_name: str
    community_address: str
    community_city: str
    community_pincode: str
    phone: str | None = None


@dataclass
class AuthTokensDTO:
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
