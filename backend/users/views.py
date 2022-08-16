from api.pagination import PageNumber
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Follow, UserProfile
from users.serializers import FollowListSerializer, UserProfileFollowSerializer


class FollowUserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        data = {'user': request.user.id, 'following': id}
        serializer = UserProfileFollowSerializer(data=data,
                                                 context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id):
        user = request.user
        following = get_object_or_404(UserProfile, id=id)
        follow = get_object_or_404(
            Follow, user=user, following=following
        )
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowListView(ListAPIView):
    pagination_class = PageNumber
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        queryset = UserProfile.objects.filter(following__user=user)
        page = self.paginate_queryset(queryset)
        serializer = FollowListSerializer(
            page, many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
