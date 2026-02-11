from sqlalchemy.ext.asyncio import AsyncSession
from tests.factories.user_factory import UserFactory


class UserBuilder:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.email: str
        self._active = True
        self._admin = False
        self._password: str

    def inactive(self):
        self._active = False
        return self

    def is_admin(self):
        self._admin = True
        return self

    def set_password(self, password: str):
        self._password = password
        return self

    def set_email(self, email: str):
        self._email = email
        return self

    async def build(self) -> UserFactory:
        user = UserFactory(email=self._email)

        self.session.add(user)
        await self.session.commit()

        return user
