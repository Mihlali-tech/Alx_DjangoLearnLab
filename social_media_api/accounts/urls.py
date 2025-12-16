from django.urls import path
from .views import RegisterView, UserProfileView, FollowUnfollowView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/<str:username>/", UserProfileView.as_view(), name="profile"),
    path("follow/<str:username>/", FollowUnfollowView.as_view(), name="follow-unfollow"),
]
