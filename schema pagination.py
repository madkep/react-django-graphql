import graphene
import json

class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    

class Query(graphene.ObjectType):
    users = graphene.List(User, limit = graphene.Int())
    hello = graphene.String()
    isAdmin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resove_is_admin(self, info):
        return True


    def resolve_users(self, info, limit=None):
        return [
            User(id="1", username="Fred"),
            User(id="2", username = "carolina")
        ][:limit]

schema = graphene.Schema(query = Query)

result = schema.execute(
    '''
    {
        users(limit:1){
            id
            username
        }
    }
    '''
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))