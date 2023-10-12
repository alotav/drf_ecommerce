from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from apps.users.models import User
from apps.users.api.serializers import UserSerializer, UserListSerializer


# con funcion y decorador
@api_view(['GET', 'POST'])
def user_api_view(request):
    
    # list (query)
    if request.method == 'GET':

        # query: traemos solo los valores que vamos a mostrar para optimizacion de la consulta
        users = User.objects.all().values('id', 'username', 'email', 'password')
        users_serializer = UserListSerializer(users, many = True) # le pasamos la consulta como param e indicamos q son todos los items
        return Response(users_serializer.data, status = status.HTTP_200_OK) # el atributo data contiene la info serializada de la consulta 

    # create
    elif request.method == 'POST':
        # print(request.data)
        users_serializer = UserSerializer(data = request.data)

        # validation
        if users_serializer.is_valid():
            users_serializer.save()
            return Response(users_serializer.data, status = status.HTTP_201_CREATED)
        return Response(users_serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT', 'DELETE'])
def user_detail_api_view(request, pk = None): # recibimos una primary key y el request
    
    #query
    user = User.objects.filter(id=pk).first() # si no lo encuentra devuelve ''

    # validation
    if user:

        # retrieve
        if request.method == 'GET':
            users_serializer = UserSerializer(user) # obtenemos solo 1, no usamos many = true
            return Response(users_serializer.data, status=status.HTTP_200_OK)

        # update
        elif request.method == 'PUT':
            users_serializer = UserSerializer(user, data = request.data)
            if users_serializer.is_valid():
                users_serializer.save()
                return Response(users_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(users_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # delete
        elif request.method == 'DELETE':
            user.delete()
            return Response({'message': "Usuario eliminado correctamente."}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No se ha encontrado un usuario con estos datos'}, status=status.HTTP_400_BAD_REQUEST)
            
    # class UserAPIView(APIView): #usando APIView

    #     def get(self, request):
    #         users = User.objects.all() # traemos a todos los usuarios
    #         users_serializer = UserSerializer(users, many = True) # le pasamos la consulta como param e indicamos q son todos los items
    #         return Response(users_serializer.data) # el atributo data contiene la info serializada de la consulta 

