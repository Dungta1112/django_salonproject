from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .models import Appointment
from .serializers import AppointmentSerializer
from accounts.permissions import IsStaffOrAdmin
import django_filters

class AppointmentFilter(django_filters.FilterSet):
    date = django_filters.DateFilter(field_name="start_time", lookup_expr='date')

    class Meta:
        model = Appointment
        fields = ['status', 'stylist', 'date']

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AppointmentFilter

    def get_queryset(self):
        user = self.request.user
        if user.role in ['staff', 'admin']:
            return Appointment.objects.all().order_by('-start_time')
        return Appointment.objects.filter(customer=user).order_by('-start_time')

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        with transaction.atomic():
            serializer.save(customer=self.request.user)

    @action(detail=True, methods=['put'])
    def cancel(self, request, pk=None):
        appointment = self.get_object()
        user = request.user
        if user.role == 'customer' and appointment.customer != user:
            return Response({"detail": "Not authorized."}, status=status.HTTP_403_FORBIDDEN)
        
        if appointment.start_time - timezone.now() < timedelta(hours=24):
            return Response({"detail": "Cannot cancel within 24 hours of appointment.", "code": "late_cancellation"}, status=status.HTTP_400_BAD_REQUEST)
        
        appointment.status = 'cancelled'
        appointment.save()
        return Response({"detail": "Appointment cancelled."})

    @action(detail=True, methods=['put'], permission_classes=[IsStaffOrAdmin])
    def confirm(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'confirmed'
        appointment.save()
        return Response({"detail": "Appointment confirmed."})

    @action(detail=True, methods=['put'], permission_classes=[IsStaffOrAdmin])
    def complete(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'completed'
        appointment.save()
        return Response({"detail": "Appointment completed."})

    @action(detail=True, methods=['put'], permission_classes=[IsStaffOrAdmin])
    def reject(self, request, pk=None):
        appointment = self.get_object()
        appointment.status = 'rejected'
        reason = request.data.get('reason', '')
        if reason:
            appointment.note = f"Rejected: {reason}\n{appointment.note or ''}"
        appointment.save()
        return Response({"detail": "Appointment rejected."})
