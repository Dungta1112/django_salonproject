from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from services.models import Service
from stylists.models import Stylist
from promotions.models import Promotion
from django.db.models import Q

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['customer', 'status', 'end_time', 'created_at']

    def validate(self, data):
        service = data.get('service')
        start_time = data.get('start_time')
        stylist = data.get('stylist')

        if start_time < timezone.now():
            raise serializers.ValidationError({"detail": "Start time cannot be in the past."})

        # Check working hours 8:00 - 20:00
        hour = start_time.hour
        end_time_est = start_time + timedelta(minutes=service.duration)
        if hour < 8 or end_time_est.hour >= 20 or (end_time_est.hour == 20 and end_time_est.minute > 0):
            raise serializers.ValidationError({"detail": "Appointments must be within working hours (08:00 - 20:00)."})

        # Check overlapping for the stylist
        if stylist:
            overlapping = Appointment.objects.filter(
                stylist=stylist,
                status__in=['pending', 'confirmed']
            ).filter(
                Q(start_time__lt=end_time_est) & Q(end_time__gt=start_time)
            )
            if overlapping.exists():
                raise serializers.ValidationError({"detail": "This time slot is already booked for the selected stylist."})

        data['end_time'] = end_time_est
        return data