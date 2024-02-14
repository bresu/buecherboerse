import django_filters
from .models import Offer


class OfferFilter(django_filters.FilterSet):

    class Meta:
        model = Offer
        fields = {
            'isbn': ['exact', 'icontains'],
            'wish_price': ['gt', 'lt', 'gte', 'lte'],
            'created_at': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'modified': ['gt', 'lt', 'gte', 'lte', 'exact', 'date'],
            'is_active': ['exact'],
            'marked': ['exact'],
            'location': ['exact', 'icontains'],  # Allows for exact matches or case-insensitive containment searches
            # Add any other fields you want to filter by
        }

        # You can also include fields directly in Meta, but for special lookup expressions (gt, lt), define them above