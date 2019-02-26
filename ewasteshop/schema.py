import graphene
import shop.schema

class Query(shop.schema.Query,graphene.ObjectType):
    pass
class Mutation(shop.schema.Mutation,graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)