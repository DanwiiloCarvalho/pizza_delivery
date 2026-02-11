from factory import Factory, Faker
from models.user import User


class UserFactory(Factory):
    class Meta:
        model = User

    name: str = Faker('first_name')
    email: str = Faker('email')
    password: str = '#Apipadoxandaonaosobemais1'
    active: bool = True
    admin: bool = False
