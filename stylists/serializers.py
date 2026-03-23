from rest_framework import serializers
from .models import Stylist

class StylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stylist
        fields = ['id', 'user', 'nickname', 'specialty', 'working_days']
        read_only_fields = ['id']
