from cryptography.fernet import Fernet, InvalidToken


class TokenVault:
    def __init__(self, key: str) -> None:
        self._fernet = Fernet(key.encode())

    def encrypt(self, token: str) -> str:
        return self._fernet.encrypt(token.encode()).decode()

    def decrypt(self, encrypted_token: str) -> str:
        try:
            return self._fernet.decrypt(encrypted_token.encode()).decode()
        except InvalidToken as error:
            raise ValueError("Stored Instagram token cannot be decrypted") from error
