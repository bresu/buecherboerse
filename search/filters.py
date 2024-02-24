from django_filters import rest_framework as filters
from django_filters import DateTimeFilter, CharFilter, BooleanFilter, NumberFilter
from django.contrib.auth.models import AnonymousUser
from search.models import Offer, Seller
from django.db.models import Q


class OfferFilter(filters.FilterSet):
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
        request = self.request

        # these are all fields that logged in users can search through using "?search=<term>"
        search_fields_dict = {
            'book_id': "__exact",
            'book__exam__name': "__icontains",
            'book__title': "__icontains",
            'book__authors': "__icontains",
            'book__publisher': "__icontains",
            'seller__fullName': "__icontains",
            'seller__matriculationNumber': '__icontains',
            'seller__email': "__icontains",
            'member__username': "__icontains",
            'member__email': "__icontains",
            'location': "__exact"
        }

        if isinstance(request.user, AnonymousUser):
            # these fields are publically searchable
            queryset = queryset.filter(active=True)
            search_fields_dict = {
                'book_id': "__exact",
                'book__exam__name': "__icontains",
                'book__title': "__icontains",
                'book__authors': "__icontains",
                'book__publisher': "__icontains",
            }

        if value:
            # Define fields to search in
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
    search = filters.CharFilter(method='global_search')

    def global_search(self, queryset, name, value):
        search_fields_dict = {
            'fullName': "__icontains",
            'matriculationNumber': '__icontains',  # @matteo wanted this
            'email': "__icontains",

        }

        if value:
            # Define fields to search in
            query = Q()
            for field, search_mode in search_fields_dict.items():
                query |= Q(**{f"{field}{search_mode}": value})
            return queryset.filter(query).distinct()
        return queryset

    class Meta:
        model = Seller
        fields = ['fullName', 'matriculationNumber', 'email']


class BookFilter(filters.FilterSet):
    exam__name = filters.CharFilter(field_name="exam__name", lookup_expr="icontains")
    maxPrice = filters.NumberFilter(field_name='maxPrice', lookup_expr='exact')
    maxPrice__gt = filters.NumberFilter(field_name="maxPrice", lookup_expr="gt")
    maxPrice__gte = filters.NumberFilter(field_name="maxPrice", lookup_expr="gte")
    maxPrice__lt = filters.NumberFilter(field_name="maxPrice", lookup_expr="lt")
    maxPrice__lte = filters.NumberFilter(field_name="maxPrice", lookup_expr="lte")
    authors = filters.CharFilter(field_name='authors',lookup_expr="icontains")
    publisher = filters.CharFilter(field_name='publisher', lookup_expr="icontains")
    search = filters.CharFilter(method='global_search')

    def global_search(self, queryset, name, value):
        search_fields_dict = {
            'isbn': "__icontains",
            'exam__name': '__icontains',  # @matteo wanted this
            'title': "__icontains",
            'authors': "__icontains"

        }
        if value:
            # Define fields to search in
            query = Q()
            for field, search_mode in search_fields_dict.items():
                query |= Q(**{f"{field}{search_mode}": value})
            return queryset.filter(query).distinct()
        return queryset

# query highlithing?
