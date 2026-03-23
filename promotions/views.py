from rest_framework import viewsets, permissions
from .models import Promotion
from .serializers import PromotionSerializer
from accounts.permissions import IsStaffOrAdmin

class PromotionViewSet(viewsets.ModelViewSet):
    serializer_class = PromotionSerializer

    def get_queryset(self):
        if self.action in ['list', 'retrieve']:
            return Promotion.objects.filter(is_active=True)
        return Promotion.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsStaffOrAdmin()]