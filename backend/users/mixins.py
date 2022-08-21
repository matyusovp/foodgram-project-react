from rest_framework import serializers
from rest_framework.serializers import Serializer

from users.models import Follow


class IsSubscribedMixin(Serializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(user=request.user, following=obj).exists()
