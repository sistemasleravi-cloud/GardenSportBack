from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Cancha, Reserva
from .serializers import CanchaSerializer, ReservaSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_superuser=False) 
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class CanchaViewSet(viewsets.ModelViewSet):
    queryset = Cancha.objects.all()
    serializer_class = CanchaSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        fecha = request.query_params.get('fecha')
        hora_inicio = request.query_params.get('hora_inicio')
        hora_fin = request.query_params.get('hora_fin')

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        canchas_data = serializer.data
        ocupadas = []

        if fecha and hora_inicio and hora_fin:
            reservas_traslapadas = Reserva.objects.filter(
                fecha=fecha,
                hora_inicio__lt=hora_fin,
                hora_fin__gt=hora_inicio
            ).exclude(estado='CANCELADA')
            ocupadas = list(reservas_traslapadas.values_list('cancha_id', flat=True))

        return Response({
            'canchas': canchas_data,
            'ocupadas': ocupadas
        })

class ReservaViewSet(viewsets.ModelViewSet):
    queryset = Reserva.objects.all()
    serializer_class = ReservaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        nombre = user.first_name if user.first_name else user.username
        serializer.save(
            usuario=user,
            nombre_cliente=nombre,
            telefono_cliente=user.email
        )