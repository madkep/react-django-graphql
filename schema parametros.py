import graphene
import uuid
import json

class Post(graphene.ObjectType):
    tittle = graphene.String()
    content = graphene.String()

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

class CreatePost(graphene.Mutation):
    post = graphene.Field(Post)

    class Arguments:
        tittle = graphene.String()
        content = graphene.String()

    def mutate(self, info,tittle,content):
        post = Post(tittle=tittle, content=content)
        return CreatePost(post=post)

class Mutation(graphene.ObjectType):
    createUser = CreateUser.Field()
    create_post = CreatePost.Field()

schema = graphene.Schema(query = Query,mutation=Mutation)

result = schema.execute(
    '''
    mutation {
        createPost(tittle:"hello", content:"world")


    }
    ''',
    variable_values={'username':'puta'}
)

dictResult = dict(result.data.items())
print(json.dumps(dictResult, indent = 2))