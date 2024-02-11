from django.urls import path, include
from rest_framework.routers import DefaultRouter
#from .views import SellerViewSet  # Assuming TransactionViewSet is commented out for now
from .views import OfferViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
# offer endpoints
router.register(r'offers', OfferViewSet, basename="offer")


# router.register(r'sellers', SellerViewSet)
# router.register(r'transactions', TransactionViewSet)  # Commented out for now

urlpatterns = [
    path('', include(router.urls)),
    path('api/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


]
