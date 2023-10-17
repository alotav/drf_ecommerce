from apps.products.models import MeasureUnit, CategoryProduct, Indicator

from rest_framework import serializers

class MeasureUnitSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasureUnit
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',) # fields, excluimos estado en vez de seleccionar todos los campos.

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryProduct
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',) # fields, excluimos estado en vez de seleccionar todos los campos.
        

class IndicadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Indicator
        exclude = ('state', 'created_date', 'modified_date', 'deleted_date',) # fields, excluimos estado en vez de seleccionar todos los campos.
        