from django_filters import rest_framework as filters
from search.models import Offer


class OfferFilter(filters.FilterSet):

    class Meta:
        model = Offer
        fields = {
            'isbn': ['exact'],
            'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
            'seller': ['exact'],
            'member': ['exact'],
            'createdAt': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'modified': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'active': ['exact'],
            'marked': ['exact'],
            'location': ['exact', 'icontains'],  # Allows for exact matches or case-insensitive containment searches
            # Add any other fields you want to filter by
        }

        # You can also include fields directly in Meta, but for special lookup expressions (gt, lt), define them above


