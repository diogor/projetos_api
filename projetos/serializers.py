from rest_framework import serializers
from .models import Projeto
from usuarios.serializers import UserSerializer



class ProjetoSerializer(serializers.ModelSerializer):
    team = UserSerializer(many=True, required=False)

    class Meta:
        model = Projeto
        exclude = ('creator',)
