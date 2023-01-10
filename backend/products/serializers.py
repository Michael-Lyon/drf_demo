from rest_framework import serializers
from rest_framework.reverse import reverse
from api.serializers import UserPublicSerializer

from products.models import Product


# class ProductsInlineSerializer(serializers.Serializer):
#     detail_url = serializers.HyperlinkedIdentityField(
    #     view_name = "products:product-detail",
    #     lookup_field = 'pk'
    # )

#     title = serializers.CharField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    edit_url = serializers.SerializerMethodField(read_only=True)
    body = serializers.CharField(source='content')
    owner = UserPublicSerializer(source='user', read_only=True)
    
    class Meta:
        model = Product
        fields = [
            "owner",
            # "url",
            "edit_url",
            "pk",
            'title',
            'body',
            'price',
            'public',
            'path',
            'endpoint',
        ]

    # CUSTOM VALIDATIONS

    def validate_title(self, value):
        qs = Product.objects.filter(title__iexact=value)
        if qs.exists():
            raise serializers.ValidationError("This content already exists.")
        return value

    # def get_detail_url(self, obj):
    #     request = self.context.get("request")
    #     if request is None:
    #         return None
    #     return reverse("product-detail", kwargs={'pk':obj.pk}, request=request, )

    def get_edit_url(self, obj):
        request = self.context.get("request")
        if request is None:
            return None
        return reverse("products:product-update", kwargs={'pk': obj.pk}, request=request, )

    
    def get_my_discount(self, obj):
        if not hasattr(obj, 'id'):
            return None

        if not isinstance(obj, Product):
            return None
        return obj.get_discount()
