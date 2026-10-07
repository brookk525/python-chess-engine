from dataclasses import dataclass

@dataclass
class UserLoginRequest:
    name: str

@dataclass
class UserLoginResponse:
    succeded: bool
    name: str

@dataclass
class UserList:
    users: list