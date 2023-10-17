from rest_framework import generics

class GeneralListApiView(generics.ListAPIView):
    serializer_class = None

    def get_queryset(self):
        model = self.get_serializer().Meta.model # obtenemos el modelo accediendo al serializador por metodo get_serializer
        return model.objects.filter(state = True)