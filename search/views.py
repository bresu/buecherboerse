from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .models import Offer, Seller, Transaction
from .serializers import OfferSerializer, SellerSerializer
from search.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import OfferFilter


class LogoutAPIView(APIView):
    """View for logging out user1, throws 401 if not logged in"""
    permission_classes = [IsAuthenticated]


    def post(self, request):
        # Perform any logout actions here (e.g., logging)
        # Since JWT is stateless, actual logout is handled by the frontend discarding the token
        return Response(status=status.HTTP_204_NO_CONTENT)


class CurrentUserAPIView(generics.RetrieveAPIView):
    """Get current user1 data (id, name, email)"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


# class OfferViewSet(viewsets.ModelViewSet):
#      queryset = Offer.objects.all()
#      serializer_class = OfferSerializer
#      permission_classes = [IsAuthenticated]
#      filter_backends = [DjangoFilterBackend]
#
#      filterset_class = OfferFilter
#      def get_queryset(self):
#          queryset = super().get_queryset()
#          print(queryset.query)  # This will print the actual SQL query being executed
#          return queryset
#      def perform_destroy(self, instance):
#          # Implement soft delete by overriding the perform_destroy method#         instance.is_active = False
# #         instance.save()

class SellerViewSet(viewsets.ModelViewSet):
    # todo: query parameters?
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]


class OfferListAPIView(ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OfferFilter
    # todo: what happens if you are not logged in!
    #filterset_fields = ('price', 'memberId')


# todo: transaction view
# class
