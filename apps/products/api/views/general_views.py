from rest_framework import viewsets
# from rest_framework import generics
# from apps.products.models import MeasureUnit, Indicator, CategoryProduct
from apps.base.api import GeneralListApiView
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, IndicadorSerializer, CategoryProductSerializer


# Generamos las vistas aplicando clases en vez de decoradores

# Heredando de clase apps.base..api.GeneralListApiView
class MeasureUnitViewSet(viewsets.ModelViewSet):
    serializer_class = MeasureUnitSerializer

class IndicatosViewSet(viewsets.ModelViewSet):
    serializer_class = IndicadorSerializer

class CategoryProductViewSet(viewsets.ModelViewSet):
    serializer_class = CategoryProductSerializer
