from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import (LogoutAPIView, CurrentUserAPIView,
                    CustomTokenObtainPairView,
                    OfferListAPIView,OfferDetailView, OfferBulkCreationView, OfferBulkDeletion,
                    SellerListApiView, SellerDetailView,
                    ExamListAPIView,
                    BookDetailView, BookListApiView)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, # not used anymore
    TokenRefreshView,
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bübö API",
        default_version='v1',
        description="Die Api der Bücherbörse",
        #terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@yourapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = SimpleRouter(trailing_slash=False)
urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # get, posten, put/ patch
    path('v1/offers', OfferListAPIView.as_view(), name="offer-list"),
    path('v1/offers/<int:pk>', OfferDetailView.as_view(), name="offer-detail"),
    path('v1/offers/bulk',OfferBulkCreationView.as_view(), name="offer-bulk-create"),
    path('v1/offers/sell', OfferBulkDeletion.as_view(), name="offer-bulk-delete"),
    path('v1/books', BookListApiView.as_view(), name='book-list'),
    path('v1/books/<int:pk>', BookDetailView.as_view(), name='book-detail'),
    path('v1/sellers', SellerListApiView.as_view(), name="seller-list"),
    path('v1/sellers/<int:pk>', SellerDetailView.as_view(), name="seller-detail"),

    path('v1/exams', ExamListAPIView.as_view(), name="exam-list"),
    path('v1/auth/login', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/auth/logout', LogoutAPIView.as_view(), name='auth_logout'),
    path('v1/auth/user', CurrentUserAPIView.as_view(), name='auth_user'),

    #path('v1/', include(router.urls)),
]