from django.conf import settings
from graphene_django import DjangoObjectType
import graphene
from .models import PersonalPost

class PersonalPostType(DjangoObjectType):
    """Describe which model we want to expose through GraphQL."""
    class Meta:
        model = PersonalPost

        # Describe the data as a node in a graph for GraphQL
        interfaces = (graphene.relay.Node, )

class Query(graphene.ObjectType):
    """Describe which records we want to show."""
    personalposts = graphene.List(PersonalPostType)

    def resolve_personalposts(self, info):
        """Decide what notes to return."""
        user = info.context.user

        if user.is_anonymous:
            return PersonalPost.objects.none()
        else:
            return PersonalPost.objects.filter(user=user)

schema = graphene.Schema(query=Query)