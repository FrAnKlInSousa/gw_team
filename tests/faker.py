from random import choice

from faker import Faker
from faker.providers import BaseProvider

fake = Faker(
    'pt_BR',
    use_weighting=False,
)


class UserType(BaseProvider):
    @staticmethod
    def user_type():
        types = ['admin', 'client']
        return choice(types)


fake.add_provider(UserType)
