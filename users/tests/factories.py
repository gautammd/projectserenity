from random import randint, uniform

import factory
from factory import LazyAttribute, LazyFunction, SubFactory, fuzzy
from factory.django import DjangoModelFactory
from faker import Factory

from users.models import User

faker = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    email = LazyAttribute(lambda o: faker.text(max_nb_chars=255))
