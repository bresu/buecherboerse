from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Seller, Offer, Transaction, Book, Exam


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class SellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = '__all__'


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    exam_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Exam.objects.all(),
        source='exam'
    )

    class Meta:
        model = Book
        fields = '__all__'


# class OfferSerializer(serializers.ModelSerializer):
#     seller = SellerSerializer(read_only=True)
#     seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), write_only=True, source='seller')
#
#     class Meta:
#         model = Offer
#         fields = ['id', 'isbn', 'price', 'marked', 'seller', 'seller_id', 'member', 'active', 'createdAt', 'modified', 'location']
#         extra_kwargs = {
#             'seller': {'read_only': True},  # Ensure seller object is read-only
#         }
#
#     def to_representation(self, instance):
#         # Start with the public data
#         ret = super().to_representation(instance)
#         request = self.context.get('request')
#
#         # Remove non-public fields for unauthenticated users
#         if not request or not request.user.is_authenticated:
#             non_public_fields = ['seller', 'member', 'active', 'createdAt', 'modified', 'location']
#             for field in non_public_fields:
#                 ret.pop(field, None)
#
#         return ret


class OfferSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Book.objects.all(),
        source='book'
    )
    seller = SellerSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Seller.objects.all(),
        source='seller'
    )
    member = UserSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=User.objects.all(),
        source='member'
    )

    class Meta:
        model = Offer
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        if not request or not request.user.is_authenticated:
            non_public_fields = ['seller', 'member', 'active', 'createdAt', 'modified', 'location']
            for field in non_public_fields:
                ret.pop(field, None)

        return ret

# pagination?
