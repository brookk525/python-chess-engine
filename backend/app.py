from __future__ import annotations

class App:
    _instance: "App | None" = None

    def __init__(self) -> None:
        if App._instance is not None:
            raise RuntimeError("Usa App.instance()")
        self.users: list[str] = []

    @classmethod
    def __instance(cls) -> "App":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def instance(cls) -> "App":
        return cls.__instance()

    def add_user(self, username: str) -> bool:
        username = (username or "").strip()
        if not username or username is None:
            return False
        if any(u.lower() == username.lower() for u in self.users):
            return False
        self.users.append(username)
        return True

    def list_users(self) -> list[str]:
        return list(self.users)