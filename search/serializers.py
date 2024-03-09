from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Seller, Offer, Transaction, Book, Exam
from simple_history.models import HistoricalRecords


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class HistoricalSellerSerializer(serializers.ModelSerializer):
    history_user_id = serializers.SerializerMethodField()

    def get_history_user_id(self, obj):
        # This method assumes you have the HistoryRequestMiddleware set up
        # and are storing the user responsible for the change.
        # Adjust according to your setup.
        return obj.history_user_id if obj.history_user else None

    class Meta:
        model = Seller.history.model  # This references the historical model for Seller
        fields = ['id', 'fullName', 'matriculationNumber', 'email', 'note', 'history_date', 'history_type',
                  'history_user_id']
        # todo: duplicate this for offers, maybe transactions as well.


class HistoricalOfferSerializer(serializers.ModelSerializer):
    history_user_id = serializers.SerializerMethodField()
    #seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', read_only=True)

    def get_history_user_id(self, obj):
        # This method assumes you have the HistoryRequestMiddleware set up
        # and are storing the user responsible for the change.
        # Adjust according to your setup.
        return obj.history_user_id if obj.history_user else None

    class Meta:
        model = Offer.history.model  # This references the historical model for Seller
        fields = [
                  'history_id',
                  'price',
                  'note',
                  'location',
                  'active',
                  'sold',
                  'history_date',
                  'history_type',
                  'history_user_id']


class SellerSerializer(serializers.ModelSerializer):
    # todo: remove this from the standard serializer.
    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        historical_records = obj.history.all()
        return HistoricalSellerSerializer(historical_records, many=True).data

    class Meta:
        model = Seller
        fields = ['id', 'fullName', 'matriculationNumber', 'email', 'note', 'history']

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

        return data

class SimpleSellerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seller
        fields = ['id', 'fullName', 'matriculationNumber', 'email', 'note']

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


class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class OfferSerializer(DynamicFieldsModelSerializer):
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=Seller.objects.all(), source='seller', write_only=True)
    book = BookSerializer(read_only=True)
    seller = SimpleSellerSerializer(read_only=True)
    history = serializers.SerializerMethodField()

    def get_history(self, obj):
        historical_records = obj.history.all()
        return HistoricalOfferSerializer(historical_records, many=True).data

    class Meta:
        model = Offer
        fields = '__all__'  # You might list specific fields if '__all__' is too broad

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        request = self.context.get('request')

        whitelist = ['book', 'price', 'marked']

        if request and not request.user.is_authenticated:
            # Create a new dictionary with only the whitelisted fields
            ret = {field: ret[field] for field in whitelist if field in ret}
            return ret
        # Determine if '/details' is in the request path
        elif 'request' in self.context and '/details' in self.context['request'].path:
            # Use all fields for '/details' endpoint
            return super().to_representation(instance)
        else:
            # Limit fields for the basic endpoint
            fields = ['id', 'book', 'price', 'active', 'sold', 'marked', 'note', 'location', 'seller','created',]
            return {field: super().to_representation(instance).get(field) for field in fields}