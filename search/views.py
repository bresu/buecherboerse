from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Offer, Seller, Transaction
from .serializers import OfferSerializer, SellerSerializer
from search.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import OfferFilter, SellerFilter


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


class SellerListApiView(ListCreateAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = SellerFilter
    ordering_fields = ['fullName', 'matriculationNumber', 'email', 'id']


class SellerDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]
    # todo doku ohne login!


class OfferListAPIView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter)
    filterset_class = OfferFilter
    ordering_fields = ['price', 'createdAt', 'modified', 'book__edition', 'location', 'marked', 'book__exam__name']
    ordering = ['-book__edition', 'price', 'createdAt']    # höchste edition, dann kleinster preis
    # todo: in der doku vermerken was default sortierung ist!

    def get_queryset(self):
        """
        Optionally restricts the returned offers to a given user,
        by filtering against query parameters in the URL.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # For unauthenticated users, ignore query parameters and return the filtered queryset
            return queryset.filter(active=True)

        # For authenticated users, apply filters based on query parameters
        # This is where you apply any filtering logic you have, which might depend on the 'filterset_class' or other custom filtering logic.
        queryset = self.filterset_class(self.request.GET, queryset=queryset, request=self.request).qs

        return queryset

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({"detail": "Anmeldedaten fehlen."},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OfferDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Optionally restricts the returned offers to a given user,
        by filtering against query parameters in the URL.
        """
        queryset = super().get_queryset()
        if not self.request.user.is_authenticated:
            # For unauthenticated users, ignore query parameters and return the filtered queryset
            return queryset.filter(active=True)

        return queryset

    def update(self, request, *args, **kwargs):
        # Ignore 'active' field changes for PATCH/PUT requests
        if 'active' in request.data:
            return Response({"detail": "Modifying the active field is not allowed."}, status=status.HTTP_403_FORBIDDEN)

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

# todo: Book View mit API support
