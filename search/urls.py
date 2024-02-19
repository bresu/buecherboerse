from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import LogoutAPIView, CurrentUserAPIView, OfferListAPIView, SellerViewSet ,OfferDetailView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = SimpleRouter(trailing_slash=False)
# offer endpoints
#router.register(r'offers', OfferViewSet, basename="offer")
router.register(r'sellers', SellerViewSet, basename="seller")
# todo: add transaction adding via api

urlpatterns = [
    path('v1/offers', OfferListAPIView.as_view(), name="offer-list"),
    path('v1/offers/<int:pk>', OfferDetailView.as_view(), name="offer-detail"),
    path('v1/auth/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/logout', LogoutAPIView.as_view(), name='auth_logout'),
    path('v1/auth/user', CurrentUserAPIView.as_view(), name='auth_user'),
    path('v1/', include(router.urls)),
]