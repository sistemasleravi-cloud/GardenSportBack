from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cancha, Reserva, Perfil

class UserSerializer(serializers.ModelSerializer):
    telefono = serializers.CharField(write_only=True, required=False)
    telefono_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'first_name', 'telefono', 'telefono_display', 'is_active']
        extra_kwargs = {'password': {'write_only': True}}

    def get_telefono_display(self, obj):
        # Verifica si el usuario tiene un perfil asociado (para no fallar con el superusuario)
        if hasattr(obj, 'perfil'):
            return obj.perfil.telefono
        return 'Sin teléfono'

    def create(self, validated_data):
        telefono = validated_data.pop('telefono', '')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', '')
        )
        # Creamos el perfil con el teléfono enlazado al usuario
        Perfil.objects.create(usuario=user, telefono=telefono)
        return user

class CanchaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cancha
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    cancha_nombre = serializers.ReadOnlyField(source='cancha.nombre')

    class Meta:
        model = Reserva
        fields = '__all__'