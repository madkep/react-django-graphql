import graphene
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from django.db.models import Q

from .models import Track, Like
from users.schema import UserType

class TrackType(DjangoObjectType):
    #se accede al modelo con el meta
    class Meta:
        model = Track

class LikeType(DjangoObjectType):
    class Meta:
        model = Like


class Query(graphene.ObjectType):
    tracks = graphene.List(TrackType, search=graphene.String())
    likes = graphene.List(LikeType)

#none es que search es opcional
    def resolve_tracks(self,info,search=None):

        if search:
            filter = (
                Q(tittle__icontains=search) |
                Q(description__icontains=search)
                
            )
                                      #nombre y matchtype tittle puede contener
                                        #exact case sensitive
                                        #iexact insensitive
                                        #gt numeros
                                        #contains contiene
                                        # icontains sin case sensitive
                                        # para filtrar multiples weas
                                        # se usa el djangoq object
                                        # Q object nos ayuda a anidad los filtros                                      
            #
            return Track.objects.filter(filter)
        return Track.objects.all() 

    def resolve_likes(self,info):
        return Like.objects.all()

class CreateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        tittle = graphene.String()
        description = graphene.String()
        url = graphene.String()
    
    def mutate(self, info, tittle, description, url):
        user = info.context.user

        if user.is_anonymous:
            raise GraphQLError('Log in to add a track')

        track = Track(tittle=tittle,description=description,url=url, posted_by=user)
        track.save()
        return CreateTrack(track=track)


class UpdateTrack(graphene.Mutation):
    track = graphene.Field(TrackType)

    class Arguments:
        track_id = graphene.Int(required=True)
        tittle = graphene.String()
        description = graphene.String()
        url = graphene.String()

    def mutate(self, info, track_id, tittle,url,description):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError('Not permited to update  hist track')
    
        track.tittle = tittle
        track.description = description
        track.url = url

        track.save()

        return UpdateTrack(track=track)


class DeleteTrack(graphene.Mutation):
    track_id = graphene.Int()

    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self, info, track_id):
        user = info.context.user
        track = Track.objects.get(id=track_id)

        if track.posted_by != user:
            raise GraphQLError('not permited to delete this track')

        track.delete()

        return DeleteTrack(track_id=track_id)



class CreateLike(graphene.Mutation):

    user = graphene.Field(UserType)
    track = graphene.Field(TrackType)


    class Arguments:
        track_id = graphene.Int(required=True)

    def mutate(self,info,track_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('login to like tracks')

        track = Track.objects.get(id=track_id)
        if not track:
            raise GraphQLError('Canot find a track with given track id')

        Like.objects.create(
            user=user,
            track=track
        )
        return CreateLike(user=user, track=track)



class Mutation(graphene.ObjectType):
    create_track = CreateTrack.Field()
    update_track = UpdateTrack.Field()
    delete_track = DeleteTrack.Field()
    create_like = CreateLike.Field()
