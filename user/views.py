from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from django.contrib.auth import logout as django_logout
from django.conf import settings
from rest_framework import status

from .serializers import CreateUserSerializer
from .serializers import RefreshTokenSerializer


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)


class SignupView(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user = serializer.save()
        # return Response({
        #     "status": CreateUserSerializer(user, context=self.get_serializer_context()).data,
        # })

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": f"User account was successfully created",
            })
        else:
            return Response({
                "Error": f" Something went wrong"
            })


class LogoutView(GenericAPIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, *args):
        sz = self.get_serializer(data=request.data)
        sz.is_valid(raise_exception=True)
        sz.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

