import graphene
from graphene import relay
from graphql import GraphQLError
from graphql_relay import from_global_id

from users.models import User
from users.types import UserNode

from .validations import validate_mutation


class UserCreateData(graphene.InputObjectType):
    email = graphene.String(required=True)


class UserUpdateData(graphene.InputObjectType):
    email = graphene.String()


class CreateUser(relay.ClientIDMutation):
    class Input:
        data = UserCreateData()

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, data=None):
        validate_dict = {
            'email': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        if data is None:
            raise GraphQLError(f'empty data')

        obj = User.objects.create(**data)

        return CreateUser(user=obj)


class UpdateUser(relay.ClientIDMutation):
    class Input:
        id = graphene.ID(required=True)
        data = UserUpdateData()

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, id, data):
        validate_dict = {
            'email': {'max': 255, },
        }

        validate_mutation(validate_dict, data)

        obj, _ = User.objects.update_or_create(
            pk=from_global_id(id)[1], defaults=data)

        return UpdateUser(user=obj)


class DeleteUser(relay.ClientIDMutation):
    class Input:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate_and_get_payload(cls, root, info, id):
        obj = User.objects.get(pk=from_global_id(id)[1])
        obj.delete()
        return DeleteUser(ok=True)
