from rest_framework import serializers

from apps.products.models import Product
# importamos los serializadores q son clave foranea para que nos muestren info en vez de id
from apps.products.api.serializers.general_serializers import MeasureUnitSerializer, CategoryProductSerializer

class ProductSerializer(serializers.ModelSerializer):
    # Metodo 1
    # los nombres de las variables deben ser iguales a las del modelo serializado
    # measure_unit = MeasureUnitSerializer()
    # category_product = CategoryProductSerializer()

    # Metodo 2: accediendo al metoso __str__ del modelo
    # measure_unit = serializers.StringRelatedField()
    # category_product = serializers.StringRelatedField()

    class Meta:
        model = Product
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',) # fields, excluimos estado en vez de seleccionar todos los campos.

    # Metodo 3: redefinir el metodo to_representation.
    def to_representation(self, instance):
        return {
            'id': instance.id,
            'description': instance.description,
            'image': instance.image if instance.image != '' else '', # validamos si no hay url a la imagen que responda ''
            'measure_unit': instance.measure_unit.description,
            'category_product': instance.category_product.description
        }