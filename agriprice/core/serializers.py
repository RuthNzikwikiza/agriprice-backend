from rest_framework import serializers
from .models import PricePrediction, Notification, Product


class PricePredictionSerializer(serializers.ModelSerializer):
    # accept product_name instead of product ID
    product_name = serializers.CharField(write_only=True)

    # show product name when returning data
    product = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = PricePrediction
        fields = [
            'id',
            'product',       # read-only (name)
            'product_name',  # write-only
            'predicted_price',
            'predicted_by',
            'reason',
            'season',
            'predicted_at',
        ]

    def create(self, validated_data):
        # extract product_name from request
        product_name = validated_data.pop('product_name')

        # get or create product
        product, _ = Product.objects.get_or_create(name=product_name)

        # attach product to validated_data
        validated_data['product'] = product

        return super().create(validated_data)


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
