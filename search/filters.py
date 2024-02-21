from django_filters import rest_framework as filters
from django_filters import DateTimeFilter, CharFilter, BooleanFilter, NumberFilter
from django.contrib.auth.models import AnonymousUser
from search.models import Offer, Seller
from django.db.models import Q


class OfferFilter(filters.FilterSet):
    # todo: make global search
    # todo: filter for datetime
    search = CharFilter(method='global_search')
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

    def global_search(self, queryset, name, value):
        if value:
            # Define fields to search in

            search_fields_dict = {
                'book_id': "__exact",
                'book__exam__name': "__icontains",
                'book__title': "__icontains",
                'book__authors': "__icontains",
                'book__publisher': "__icontains",
                'seller__fullName': "__icontains",
                'seller__matriculationNumber': '__exact',
                'seller__email': "__icontains",
                'member__username': "__icontains",
                'member__email': "__icontains",
                'location': "__exact"
            }
            query = Q()
            for field, search_mode in search_fields_dict.items():
                query |= Q(**{f"{field}{search_mode}": value})
            return queryset.filter(query).distinct()
        return queryset

    def filter_for_authenticated_users(self, queryset, name, value):
        request = self.request
        if isinstance(request.user, AnonymousUser):
            return queryset.filter(active=True)  # only active offers should be publicly available
        # Apply filter if user is authenticated
        return queryset.filter(**{name: value})

    class Meta:
        model = Offer
        fields = {
            'book__isbn': ['exact'],
            'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'marked': ['exact'],
        }


class SellerFilter(filters.FilterSet):
    fullName = filters.CharFilter(field_name="fullName", lookup_expr='icontains')
    matriculationNumber = filters.CharFilter(field_name="matriculationNumber", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')

    class Meta:
        model = Seller
        fields = ['fullName', 'matriculationNumber', 'email']

    # todo: global search :-(
    # query highlighting?
