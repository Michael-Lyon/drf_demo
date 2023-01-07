from django.shortcuts import render
from django.http import JsonResponse
from django.forms import model_to_dict
from products.models import Product
from rest_framework.response import Response
from rest_framework.decorators import api_view

from products.serializers import ProductSerializer

# Create your views here.


@api_view(['POST'])
def api_home(request, *args, **kwargs):
    """DRF API VIEW"""
    data = {}
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        # instance = serializer.save()
        data = serializer.data
        return Response({'message': data})
    return Response({'message':'Invalid data'}, status=400)


