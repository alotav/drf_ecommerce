from django.urls import path

from apps.products.api.views.general_views import MeasureUnitListAPIView, IndicatosListAPIView, CategoryProductListAPIView
from apps.products.api.views.product_views import ProductListAPIView, ProductCreateAPIView


urlpatterns = [
    path('measure_unit/', MeasureUnitListAPIView.as_view(), name = 'measure_unit'),
    path('indicator/', IndicatosListAPIView.as_view(), name = 'indicator'),
    path('category_product/', CategoryProductListAPIView.as_view(), name = 'category_product'),
    path('product/list/', ProductListAPIView.as_view(), name = 'product_list'),
    path('product/create/', ProductCreateAPIView.as_view(), name = 'product_create'),
]