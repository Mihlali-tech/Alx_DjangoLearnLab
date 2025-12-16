from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User = get_user_model()

class FollowUnfollowView(generics.GenericAPIView):
    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user in target_user.followers.all():
            target_user.followers.remove(request.user)
            action = "unfollowed"
        else:
            target_user.followers.add(request.user)
            action = "followed"

        return Response({"status": action}, status=status.HTTP_200_OK)
