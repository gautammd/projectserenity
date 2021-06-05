import graphene
from graphene import relay
from graphene_django import DjangoObjectType

from .models import User


class UserNode(DjangoObjectType):

    class Meta:
        model = User
        interfaces = (relay.Node, )
        fields = ['id', 'email']
        filter_fields = ['id', 'email']
