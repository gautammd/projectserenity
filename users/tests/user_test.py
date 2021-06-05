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

    def test_create_user(self):
        """
        Ensure we can create a new user object.
        """

        user_dict = camelize(factory.build(dict, FACTORY_CLASS=UserFactory))

        response = self.query(
            """
            mutation($input: CreateUserInput!) {
                createUser(input: $input) {
                    clientMutationId,
                    user {
                        id
                        email
                    }
                }
            }
            """,
            input_data={'data': user_dict}
        )
        content = json.loads(response.content)
        generated_user = content['data']['createUser']['user']
        self.assertResponseNoErrors(response)
        self.assertEquals(user_dict['email'], generated_user['email'])

    def test_fetch_all(self):
        """
        Create 3 objects, fetch all using allUser query and check that the 3 objects are returned following
        Relay standards.
        """
        response = self.query(
            """
            query {
                allUser{
                    edges{
                        node{
                            id
                            email
                        }
                    }
                }
            }
            """
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        user_list = content['data']['allUser']['edges']
        user_list_qs = User.objects.all()
        for i, edge in enumerate(user_list):
            user = edge['node']
            self.assertEquals(user['id'], to_global_id(
                UserNode._meta.name, user_list_qs[i].id))
            self.assertEquals(user['email'], user_list_qs[i].email)

    def test_delete_mutation(self):
        """
        Create 3 objects, fetch all using allUser query and check that the 3 objects are returned.
        Then in a loop, delete one at a time and check that you get the correct number back on a fetch all.
        """
        list_query = """
            query {
                allUser{
                    edges{
                        node{
                            id
                        }
                    }
                }
            }
            """
        response = self.query(list_query)
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        user_list = content['data']['allUser']['edges']
        user_count = len(user_list)
        for i, edge in enumerate(user_list, start=1):
            user = edge['node']
            user_id = user['id']
            response = self.query(
                """
                mutation($input:DeleteUserInput!) {
                   deleteUser(input: $input)
                   {
                       ok
                    }
                }
                """, input_data={'id': user_id})
            response = self.query(list_query)
            content = json.loads(response.content)
            user_list = content['data']['allUser']['edges']
            new_len = len(user_list)
            assert user_count - i == new_len

    def test_update_mutation_correct(self):
        """
        Add an object. Call an update with 2 (or more) fields updated.
        Fetch the object back and confirm that the update was successful.
        """
        user = UserFactory.create()
        user_id = to_global_id(UserNode._meta.name, user.pk)
        user_dict = factory.build(dict, FACTORY_CLASS=UserFactory)
        response = self.query(
            """
            mutation($input: UpdateUserInput!){
                updateUser(input: $input) {
                    user{
                        email
                    }
                }
            }
            """,
            input_data={
                'id': user_id,
                'data': {
                    'email': user_dict['email'],
                }
            }
        )
        self.assertResponseNoErrors(response)
        parsed_response = json.loads(response.content)
        updated_user_data = parsed_response['data']['updateUser']['user']
        self.assertEquals(updated_user_data['email'], user_dict['email'])

    def test_update_mutation_email_with_incorrect_value_data_type(self):
        """
        Add an object. Call an update with 2 (or more) fields updated with values that are expected to fail.
        Fetch the object back and confirm that the fields were not updated (even partially).
        """
        user = UserFactory.create()
        user_id = to_global_id(UserNode._meta.name, user.pk)
        random_int = faker.pyint()
        response = self.query(
            """
            mutation{
                updateUser(input: {
                    id: "%s",
                    data:{
                        email: %s
                    }
                }) {
                    user{
                        email
                    }
                }
            }
            """
            % (user_id, random_int)
        )
        self.assertResponseHasErrors(response)
