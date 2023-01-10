from django.urls import path
from . import views


app_name = "products"

urlpatterns = [
    # path("", views.product_alt_view),
    path("", views.ProductListCreateApiView.as_view(), name="product_list"),
    path("<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("<int:pk>/update/", views.ProductUpdatelView.as_view(), name="product-update"),
    path("<int:pk>/delete/", views.ProductDeletelView.as_view()),
]
