from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer

User = get_user_model()

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = [permissions.IsAuthenticated]

class FollowUnfollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, username):
        try:
            target_user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        if request.user == target_user:
            return Response({"error": "You cannot follow/unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user in target_user.followers.all():
            target_user.followers.remove(request.user)
            return Response({"status": f"You have unfollowed {username}"})
        else:
            target_user.followers.add(request.user)
            return Response({"status": f"You are now following {username}"})
