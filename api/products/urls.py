
from django.urls import path
from products import views

app_name = 'products'

urlpatterns = [
    path("models/",views.PvModel.as_view({'get':'list'}),name="Model"),
    path("models/",views.PvModel.as_view({'post':'post'}),name="Add Model"),
    path("models/<str:pk>",views.PvModel.as_view({'put':'put'}),name="Update Model"),
    path("models/<str:pk>",views.PvModel.as_view({'delete':'delete'}),name="Delete Model"),
    path("model/<str:pk>",views.PvModelList.as_view({'get': 'list'}),name="Retrieve Model"),

    path("product/",views.PvProduct.as_view({'get':'list'}),name="Product"),
    path("product/",views.PvProduct.as_view({'post':'post'}),name="Add Product"),
    path("product/<str:pk>",views.PvProduct.as_view({'put':'put'}),name="Update Product"),
    path("product/<str:pk>",views.PvProduct.as_view({'delete':'delete'}),name="Delete Product"),
    path("product/<str:pk>",views.PvProductList.as_view({'get': 'get'}),name="Retrieve Product"),

    path("module-product/<str:pk>",views.ModuleProductList.as_view({'get':'list'}),name="Product Modules")

    ]

