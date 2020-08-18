import graphene
import uuid
import json

class User(graphene.ObjectType):
    id = graphene.ID(default_value=str(uuid.uuid4()))
    username = graphene.String()
    

class Query(graphene.ObjectType):
    users = graphene.List(User)
    hello = graphene.String()
    isAdmin = graphene.Boolean()

    def resolve_hello(self, info):
        return "world"

    def resove_is_admin(self, info):
        return True


    def resolve_users(self, info):
        return [
            User(id="1", username="Fred"),
            User(id="2", username = "carolina")
        ]


class CreateUser(graphene.Mutation):
    #se instacia el modelo
    user = graphene.Field(User)

    #para agregar argumentos a la mutacion
    class Arguments:
        username = graphene.String()
    
    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()

schema = graphene.Schema(query = Query,mutation=Mutation)

result = schema.execute(
    '''
    mutation{
        createUser(username:"jeff"){
            user{
                id
                username
            }
        }
    }
    '''
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))