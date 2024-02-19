from django_filters import rest_framework as filters
from django_filters import DateTimeFilter, CharFilter, BooleanFilter, NumberFilter
from django.contrib.auth.models import AnonymousUser
from search.models import Offer, Seller

class OfferFilter(filters.FilterSet):
    location = CharFilter(field_name="location", method='filter_for_authenticated_users')
    active = BooleanFilter(field_name="active", method="filter_for_authenticated_users")
    member = NumberFilter(field_name="member", method="filter_for_authenticated_users")
    seller = NumberFilter(field_name="seller", method="filter_for_authenticated_users")
    createdAt = DateTimeFilter(field_name='createdAt', lookup_expr='exact', method='filter_for_authenticated_users')
    createdAt__gt = DateTimeFilter(field_name='createdAt', lookup_expr='gt', method='filter_for_authenticated_users')
    createdAt__lt = DateTimeFilter(field_name='createdAt', lookup_expr='lt', method='filter_for_authenticated_users')
    createdAt__gte = DateTimeFilter(field_name='createdAt', lookup_expr='gte', method='filter_for_authenticated_users')
    createdAt__lte = DateTimeFilter(field_name='createdAt', lookup_expr='lte', method='filter_for_authenticated_users')
    modified = DateTimeFilter(field_name='modified', lookup_expr='exact', method='filter_for_authenticated_users')
    modified__gt = DateTimeFilter(field_name='modified', lookup_expr='gt', method='filter_for_authenticated_users')
    modified__lt = DateTimeFilter(field_name='modified', lookup_expr='lt', method='filter_for_authenticated_users')
    modified__gte = DateTimeFilter(field_name='modified', lookup_expr='gte', method='filter_for_authenticated_users')
    modified__lte = DateTimeFilter(field_name='modified', lookup_expr='lte', method='filter_for_authenticated_users')

    def filter_for_authenticated_users(self, queryset, name, value):
        request = self.request
        if isinstance(request.user, AnonymousUser):
            return queryset.filter(active=True)  # only active offers should be publicly available
        # Apply filter if user is authenticated
        return queryset.filter(**{name: value})

    class Meta:
        model = Offer
        fields = {
            'isbn': ['exact'],
            'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'marked': ['exact'],
        }


class SellerFilter(filters.FilterSet):
    class Meta:
        model = Seller
        fields = {
            'fullName': ['icontains'],
            'matriculationNumber': ["icontains"],
            'email': ['icontains']
        }