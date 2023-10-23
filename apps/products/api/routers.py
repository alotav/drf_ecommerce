from rest_framework.routers import DefaultRouter
from apps.products.api.views.product_viewsets import ProductViewSet
from apps.products.api.views.general_views import *
# instanciamos router
router = DefaultRouter()

# creamos la ruta
router.register(r'products', ProductViewSet, basename='products')
router.register(r'measure-unit', MeasureUnitViewSet, basename='measure_unit')
router.register(r'indicators', IndicatosViewSet, basename='indicators')
router.register(r'category-products', CategoryProductViewSet, basename='category_products')

# asociamos las urls a las rutas
urlpatterns = router.urls