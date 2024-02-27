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

    def validate(self, data):
        instance = self.instance  # self.instance is available in serializers during updates

        # Check if the matriculationNumber is provided and is not unique, except for the current instance
        matriculation_number = data.get('matriculationNumber')
        if matriculation_number:
            existing_with_matriculation = Seller.objects.filter(matriculationNumber=matriculation_number).exclude(
                pk=instance.pk if instance else None)
            if existing_with_matriculation.exists():
                raise serializers.ValidationError(
                    {"matriculationNumber": "A seller with this matriculation number already exists."})

        # def validate(self, data):
    #     # Check if the matriculationNumber is provided and is not unique
    #     matriculation_number = data.get('matriculationNumber')
    #     if matriculation_number and Seller.objects.filter(matriculationNumber=matriculation_number).exists():
    #         raise serializers.ValidationError(
    #             {"matriculationNumber": "A seller with this matriculation number already exists."})

        # Check if the email is not unique
        # email = data.get('email')
        # if Seller.objects.filter(email=email).exists():
        #     raise serializers.ValidationError({"email": "A seller with this email already exists."})

        return data


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    exam = ExamSerializer(read_only=True)
    exam_id = serializers.PrimaryKeyRelatedField(
        write_only=True,
        queryset=Exam.objects.all(),
        source='exam',
        required=False,
        allow_null=True
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

        whitelist = ['book', 'price', 'marked']

        if request and not request.user.is_authenticated:
            # Create a new dictionary with only the whitelisted fields
            ret = {field: ret[field] for field in whitelist if field in ret}
        return ret

# pagination?
