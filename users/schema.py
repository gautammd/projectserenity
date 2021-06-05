from graphene import ObjectType, relay
from graphene_django.filter import DjangoFilterConnectionField

from .mutations.user import CreateUser, DeleteUser, UpdateUser
from .types import UserNode


class Query(ObjectType):
    user = relay.Node.Field(UserNode)

    all_user = DjangoFilterConnectionField(UserNode)


class Mutation(ObjectType):
    create_user = CreateUser.Field()

    update_user = UpdateUser.Field()

    delete_user = DeleteUser.Field()
