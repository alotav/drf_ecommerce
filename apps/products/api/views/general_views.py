from rest_framework import generics
from apps.products.models import MeasureUnit, Indicator, CategoryProduct
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicadorSerializer, CategoryProductSerializer

from apps.base.api import GeneralListApiView

# Generamos las vistas aplicando clases en vez de decoradores

# Heredando de clase apps.base..api.GeneralListApiView
class MeasureUnitListAPIView(GeneralListApiView):
    serializer_class = MeasureUnitSerializer

class IndicatosListAPIView(GeneralListApiView):
    serializer_class = IndicadorSerializer

class CategoryProductListAPIView(GeneralListApiView):
    serializer_class = CategoryProductSerializer


# PRIMER CODIGO SIN HABER HECHO GeneralListApiView EN BASE API:
# listAPIView en una clase generica que tiene DRF para listar informacion.
# Con esto obtendremos las unidades de medida listadas en formato JSON

# class MeasureUnitListAPIView(generics.ListAPIView):
#     serializer_class = MeasureUnitSerializer


#     def get_queryset(self):
#         return MeasureUnit.objects.filter(state=True) # filtramos para traer los que no estan eliminados.

# class IndicatosListAPIView(generics.ListAPIView):
#     serializer_class = IndicadorSerializer


#     def get_queryset(self):
#         return Indicator.objects.filter(state=True) # filtramos para traer los que no estan eliminados.

# class CategoryProductListAPIView(generics.ListAPIView):
#     serializer_class = CategoryProductSerializer


#     def get_queryset(self):
#         return CategoryProduct.objects.filter(state=True) # filtramos para traer los que no estan eliminados.