from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer

from products.models import Product




class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    # url = serializers.SerializerMethodField(read_only=True)
    edit_url = serializers.SerializerMethodField(read_only=True)
    detail_url = serializers.HyperlinkedIdentityField(
        view_name="product_detail",
        lookup_field='pk'
    )
    owner = UserPublicSerializer(source='user',read_only=True)
    class Meta:
        model = Product
        fields = [
            "owner",
            # "url",
            "detail_url",
            "edit_url",
            "pk",
            'title',
            'content',
            'price',
            'sale_price',
            'my_discount',
        ]
    
    
    # CUSTOM VALIDATIONS
    def validate_title(self, value):
        qs = Product.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("This content already exists.")
        return value
    
    def get_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product_detail", kwargs={'pk':obj.pk}, request=request, )
    
    def get_edit_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("product_update", kwargs={'pk':obj.pk}, request=request, )

    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None

        if not isinstance(obj, Product):
            return None
        return obj.get_discount()