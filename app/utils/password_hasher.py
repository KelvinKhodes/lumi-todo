from argon2 import PasswordHasher as ArgonPasswordHasher

class PasswordHasher:
    def __init__(self, hasher: ArgonPasswordHasher):
        self._hasher: ArgonPasswordHasher = hasher

    def hash_password(self, raw: str) -> str:
        return self._hasher.hash(raw)

    def verify(self, raw: str, hash: str) -> bool:
        return self._hasher.verify(hash, raw)