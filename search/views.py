from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Offer
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the active offers
        for the currently authenticated user.
        """
        return Offer.objects.filter(is_active=True)

    def perform_destroy(self, instance):
        # Implement soft delete by overriding the perform_destroy method
        instance.is_active = False
        instance.save()