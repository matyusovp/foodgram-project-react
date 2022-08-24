from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.models import Recipe
from users.mixins import IsSubscribedMixin
from users.models import Follow, UserProfile


class UserProfileSerializer(UserSerializer, IsSubscribedMixin):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = (
            'id', 'last_name', 'username', 'first_name',
            'email', 'is_subscribed'
        )


class UserProfileFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Вы уже подписаны')
            )
        ]

    def validate(self, data):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        following = data['following']
        if request.user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя!'
            )
        return data


class UserProfileCreateSerializer(UserCreateSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email', 'username', 'password')


class RecipeFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer, IsSubscribedMixin):
    recipes_count = serializers.SerializerMethodField(read_only=True)
    recipes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    def get_recipes(self, obj):
        request = self.context.get('request')
        recipes_limit = request.query_params.get('recipes_limit')
        if not request or request.user.is_anonymous:
            return False
        if recipes_limit:
            recipes = Recipe.objects.filter(
                author=obj.author_id).all()[:(int(recipes_limit))]
        else:
            recipes = Recipe.objects.filter(author=obj.author_id).all()
        context = {'request': request}
        return RecipeFollowSerializer(
            recipes, many=True, context=context).data

    def get_recipes_count(self, obj):
        return obj.recipes.count()
