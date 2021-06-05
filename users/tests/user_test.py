import json
import random
from datetime import datetime

import factory
from faker import Factory
from graphene_django.utils.testing import GraphQLTestCase
from graphene_django.utils.utils import camelize
from graphql_relay import to_global_id

from users.models import User
from users.types import UserNode

from .factories import UserFactory

faker = Factory.create()


class User_Test(GraphQLTestCase):
    def setUp(self):
        self.GRAPHQL_URL = "/graphql"
        UserFactory.create_batch(size=3)
    
    pass
