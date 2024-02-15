from django_filters import rest_framework as filters
from search.models import Offer


class OfferFilter(filters.FilterSet):
    seller = filters.NumberFilter(method='filter_seller')
    member = filters.NumberFilter(method='filter_member')

    def filter_seller(self, queryset, name, value):
        """
        Custom filter method to filter offers by seller without enforcing existence check.
        """
        # Ensure that the value is treated as an integer for filtering
        try:
            value_int = int(value)  # Attempt to convert value to integer
            return queryset.filter(**{name: value_int})
        except (ValueError, TypeError):
            return queryset  # If conversion

    def filter_member(self, queryset, name, value):
        try:
            value_int = int(value)  # Attempt to convert value to integer
            return queryset.filter(**{name: value_int})
        except (ValueError, TypeError):
            return queryset  # If conversion

    class Meta:
        model = Offer
        fields = {
            'isbn': ['exact'],
            'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'seller': ['exact'],
            'member': ['exact'],
            # todo: iso-format
            'createdAt': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'modified': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'active': ['exact'],
            'marked': ['exact'],
            'location': ['exact', 'icontains'],  # Allows for exact matches or case-insensitive containment searches
            # Add any other fields you want to filter by
        }

        # You can also include fields directly in Meta, but for special lookup expressions (gt, lt), define them above
