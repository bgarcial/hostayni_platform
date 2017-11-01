from django.utils.timesince import timesince
from rest_framework import serializers

from accounts.api.serializers import UserDisplaySerializer
from posts.models import Post # from ..models import

class ParentPostModelSerializer(serializers.ModelSerializer):
    # user = UserDisplaySerializer()
    user = UserDisplaySerializer(read_only=True) # write_only
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    # Para dar like a un post padre o a un repost, se declaran aca tambien
    # likes y did_like, y tendra ambito sobre ambos, post o repost.
    likes = serializers.SerializerMethodField()

    # ****
    did_like = serializers.SerializerMethodField()
    # ****

    class Meta:
        model = Post
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'likes',

            # ****
            'did_like',
            # ****
        ]

    '''
    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request
        if user in obj.liked.all():
            return True
        return False
    '''

    def get_did_like(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False


    def get_likes(self, obj):
        # Tomamos el campo liked en el modelo Post y
        # le hacemos un count para contar los likes
        return obj.liked.all().count()

    def get_date_display(self, obj):
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        # view parameters %b
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"


# Los posts que tienen valor en el atributo parent en /api/post
# es porque son reposteados, los que no, son post originales
class PostModelSerializer(serializers.ModelSerializer):

    parent_id = serializers.CharField(write_only=True, required=False)
    # user = UserDisplaySerializer()
    user = UserDisplaySerializer(read_only=True) # write_only
    date_display = serializers.SerializerMethodField()
    timesince = serializers.SerializerMethodField()

    # para que desde api y desde web solo se grabe un post sin neesidad de asociarle el parent
    # pues ser aun post original y no un post para ir anidado a un parent
    parent = ParentPostModelSerializer(read_only=True)

    likes = serializers.SerializerMethodField()

    # ****
    did_like = serializers.SerializerMethodField()
    # ****

    class Meta:
        model = Post
        fields = [
            'parent_id',
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'parent',
            'likes',

            # ****
            'did_like',
            # ****

            # Se responde a un post padre
            'reply',

        ]

        # read_only_fields = ['reply',]

    # ****

    # Se ha cambiado get_did_like por el metodo de abajo
    # acorde a esta respuesta https://www.udemy.com/tweetme-django/learn/v4/questions/2789020
    # Y mas adelante lo arreglan asi: https://www.udemy.com/tweetme-django/learn/v4/t/lecture/6139532?start=0
    def get_did_like(self, obj):
        request = self.context.get("request")
        try:
            user = request.user
            if user.is_authenticated():
                if user in obj.liked.all():
                    return True
        except:
            pass
        return False

    # ****
    '''
    def get_did_like(self, obj):
        request = self.context.get("request")
        user = request
        if user in obj.liked.all():
            return True
        return False
    '''
    def get_likes(self, obj):
        # Tomamos el campo liked en el modelo Post y
        # le hacemos un count para contar los likes
        return obj.liked.all().count()

    '''
    def get_is_repost(self, obj):
        # Averiguamos si es un post original o no. Si tiene parent es reposteado
        # y retornamos True
        if obj.parent:
            return True
        # sino tiene parent retornamos False, y sera un post original
        return False
    '''

    def get_date_display(self, obj):
        # https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior
        # view parameters %b
        return obj.timestamp.strftime("%b %d, %Y at %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + " ago"

