from rest_framework import generics
from products.models import Product
from products.serializers import ProductSerializer

class SearchLIstView(generics.ListAPIView):
    queryset = Product.objects.all()
