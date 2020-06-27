from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Projeto
from .serializers import ProjetoSerializer


class ProjetoViewSet(ModelViewSet):
    serializer_class = ProjetoSerializer
    queryset = Projeto.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Projeto.objects.for_user(self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def update(self, request, *args, **kwargs):
        projeto = self.get_object()

        if request.user.id != projeto.creator.id:
            raise PermissionDenied()

        super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        raise PermissionDenied()
