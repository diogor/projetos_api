from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied()

        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id != request.user.id:
            raise PermissionDenied()

        self.serializer_class = UserUpdateSerializer
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer):
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            serializer.save(password=make_password(password))

    def check_permissions(self, request):
        if request.method == 'POST':
            return
        super().check_permissions(request)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.id != request.user.id:
            raise PermissionDenied()

        serializer = self.get_serializer(instance)

        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied()
