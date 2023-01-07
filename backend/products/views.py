from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer

from api.mixins import StaffEditorPeermissionMixin, UserQuerySetMixin


class ProductListCreateApiView(UserQuerySetMixin,
                               StaffEditorPeermissionMixin,
                               generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # allow_saff_view = True

    # No need again cuz it's already in the default settings
    # authentication_classes = [
    #     TokenAuthentication,
    #     authentication.SessionAuthentication,

    # ]
    #  No longer needed since it's in the mixin now
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        """How to add additional context to the create view if u needed to work with the data before saving"""

        # serializer.save()
        print(serializer.validated_data)
        title = serializer.validated_data.get('title', None)
        content = serializer.validated_data.get('content', None)

        if content is None:
            content = title

        serializer.save(user=self.request.user, content=content)
        # you could send a signal

    # def get_queryset(self, *args, **kwargs):
    #     request = self.request
    #     qs = super().get_queryset(*args, **kwargs)
    #     print(request.user)
    #     return qs.filter(user=request.user)


class ProductDetailView(StaffEditorPeermissionMixin,
                        generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'


class ProductUpdatelView(StaffEditorPeermissionMixin,
                         generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title


class ProductDeletelView(StaffEditorPeermissionMixin,
                         generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        #  before destroying you can do anything you want with the instance here.
        return super().perform_destroy(instance)


# class ProductListAPIView(generics.ListAPIView):

# A single view that can handle POST, GET
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method
    queryset = Product.objects.all()

    if method == 'GET':
        if pk is not None:
            # detail view
            # raise a 404 if not exists
            obj = get_object_or_404(Product, pk=pk)
            data = ProductSerializer(obj, many=False)
            return Response(data)
        # list view
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    # POST METHOD
    if method == 'POST':
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title', None)
            content = serializer.validated_data.get('content') or None

            if content is None:
                content = title
            serializer.save(content=content)
            return Response(serializer.data)
        return Response({'message': "Invalid data"})
        # you could send a signal
