from rest_framework import viewsets
from .models import Inquiry
from .serializers import InquirySerializer

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all().select_related("property", "user")
    serializer_class = InquirySerializer
