from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CreateUserSerializer


class SignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CreateUserSerializer


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh'))
        refresh_token.blacklist()
        return Response("Successful Logout", status=status.HTTP_200_OK)

