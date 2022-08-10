from django.urls import include, path

from users.views import FollowUserProfileView, FollowListView

urlpatterns = [
    path('users/<int:id>/subscribe/', FollowUserProfileView.as_view(),
         name='subscribe'),
    path('users/subscriptions/', FollowListView.as_view(),
         name='subscriptions'),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include('djoser.urls')),
]