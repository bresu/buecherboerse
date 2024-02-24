from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (LogoutAPIView, CurrentUserAPIView, OfferListAPIView,OfferDetailView,
                    CustomTokenObtainPairView,

                    SellerListApiView, SellerDetailView, BookDetailView, BookListApiView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # not used anymore
    TokenRefreshView,
)

router = SimpleRouter(trailing_slash=False)
urlpatterns = [
    # get, posten, put/ patch
    path('v1/offers', OfferListAPIView.as_view(), name="offer-list"),
    path('v1/offers/<int:pk>', OfferDetailView.as_view(), name="offer-detail"),
    # todo: endpoint for bulk-deletion of offers "/sell + POST" geht no ned
    # path('v1/offers/sell')
    path('v1/books', BookListApiView.as_view(), name='book-list'),
    path('v1/books/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('v1/sellers', SellerListApiView.as_view(), name="seller-list"),
    path('v1/sellers/<int:pk>', SellerDetailView.as_view(), name="seller-detail"),
    path('v1/auth/login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/logout', LogoutAPIView.as_view(), name='auth_logout'),
    path('v1/auth/user', CurrentUserAPIView.as_view(), name='auth_user'),

    #path('v1/', include(router.urls)),
]