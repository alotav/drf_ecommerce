from rest_framework import generics
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from apps.users.authentication_mixins import Authentication
from apps.base.api import GeneralListApiView
from apps.products.api.serializers.product_serializers import ProductSerializer

# VIEWSET:
class ProductViewSet(Authentication, viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    
    #queryset = ProductSerializer.Meta.model.objects.filter(state=True)
    
    # queryset
    def get_queryset(self, pk=None):
            if pk is None:
                return self.get_serializer().Meta.model.objects.filter(state=True)
            
            return self.get_serializer().Meta.model.objects.filter(id=pk,state=True).first()

    def list(self, queryset):
        print('Hola desde listado')
        product_serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)


    # CREATE (POST)
    def create(self, request):
        # enviamos info al serializador
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Producto creado correctamente'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    # UPDATE (PUT)
    def update(self, request, pk=None):
        if self.get_queryset(pk):
            product_serializer = self.serializer_class(self.get_queryset(pk), data = request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status = status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    # DESTROY (DELETE)
    # reescribimos el metodo delete para que haga eliminacion logica y no borrado en la DB
    def destroy(self, request, pk=None):
        product = self.get_queryset().filter(id=pk).first()
        if product:
            product.state = False
            product.save()
            return Response({'message':'Producto eliminado correctamente!'}, status=status.HTTP_200_OK)
        return Response({'message':'No existe producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST)



# class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = ProductSerializer
    
    

#         # reescribimos metodo patch de UpdateAPIView
#     def patch(self, request, pk=None):
#         if self.get_queryset(pk):
#             # le pasamos el serializador:
#             product_serializer = self.serializer_class(self.get_queryset(pk))
#             return Response(product_serializer.data, status=status.HTTP_200_OK)
#         return Response({'message':'No existe producto con estos datos'}, status=status.HTTP_400_BAD_REQUEST)







