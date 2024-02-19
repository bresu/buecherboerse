from rest_framework import viewsets, status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
#from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Offer, Seller, Transaction
from .serializers import OfferSerializer, SellerSerializer
from search.serializers import UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
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


class SellerViewSet(viewsets.ModelViewSet):
    # todo: query parameters?
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = SellerFilter


class OfferListAPIView(ListCreateAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OfferFilter

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

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    # todo: patch/put darf nicht active ändern
    # todo: id soll in reposne bei beiden views sein

