from rest_framework import viewsets
from .models import Stylist
from .serializers import StylistSerializer

class StylistViewSet(viewsets.ModelViewSet):
    queryset = Stylist.objects.all().order_by('id')
    serializer_class = StylistSerializer
