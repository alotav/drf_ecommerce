from django.contrib.sessions.models import Session

from datetime import datetime

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.authentication_mixins import Authentication
from apps.users.api.serializers import UserTokenSerializer

class UserToken(Authentication, APIView):
    """
    Validate Token
    """
    def get(self,request,*args,**kwargs):
        
        try:
            user_token, _ = Token.objects.get_or_create(user = self.user)
            user = UserTokenSerializer(self.user)
            return Response({
                'token' : user_token.key,
                'user': user.data
                })
        except:
            return Response({
                'error': 'Credenciales enviadas incorrectas.'
            }, status=status.HTTP_400_BAD_REQUEST)

class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data, context={'request':request})
        if login_serializer.is_valid():
            print("paso validacion")
            # print(login_serializer.validated_data['user'])
            user = login_serializer.validated_data['user']
            if user.is_active:
                # si el usuario esta activo creamos un Token:
                # declaramos dos variables, el metodo get_or_create(usuario) toma como parametro un usuario y retorna la instancia y un booleano. Este ultimo sera el valor de "creater", el otro el del 'token'
                token,created = Token.objects.get_or_create(user = user)
                user_serializer = UserTokenSerializer(user)
                
                # si created == true retornamos response:
                if created:
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso',
                    }, status = status.HTTP_201_CREATED)
                else:
                    # obtenemos todas las sesiones
                    all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) # tiempo mayor o igual que
                    if all_sessions.exists():
                        # si coincide el id del usuario con el id de la sesion entonces la borramos
                        for session in all_sessions:
                            session_data = session.get_decoded()
                            if user.id == int(session_data.get('_auth_user_id')):
                                session.delete()
                    # si no fue creado es porque ya tiene token
                    # entonces lo borramos y volvemos a crear
                    token.delete()
                    token = Token.objects.create(user = user)
                    # y devolvemos la rta
                    return Response({
                        'token': token.key,
                        'user': user_serializer.data,
                        'message': 'Inicio de sesion exitoso',
                    }, status = status.HTTP_201_CREATED)
                    # token.delete()
                    # return Response({
                    #     'error':'Ya se ha iniciado sesion con este usuario'
                    # }, status=status.HTTP_409_CONFLICT)
            else:
                return Response({'error': 'Este usuario no puede iniciar sesion.'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
                return Response({'error': 'Nombre de usuario o contraseña incorrectos.'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Hola desde response'}, status=status.HTTP_200_OK)


class Logout(APIView):
    
    def get(self, request, *args, **kwargs):

        try:
            # recibimos el token desde en front en variable token
            token = request.GET.get('token')
            print(token)
            token = Token.objects.filter(key=token).first()

            if token:
                user = token.user

                all_sessions = Session.objects.filter(expire_date__gte = datetime.now()) # tiempo mayor o igual que
                if all_sessions.exists():
                    # si coincide el id del usuario con el id de la sesion entonces la borramos
                    for session in all_sessions:
                        session_data = session.get_decoded()
                        if user.id == int(session_data.get('_auth_user_id')):
                            session.delete()
                
                token.delete()

                session_message = 'Sesion de usuario eliminada'
                token_message = 'Token eliminado'
                return Response({'token_message': token_message, 'session_message': session_message}, status=status.HTTP_200_OK)

            return Response({'error': 'No se ha encontrado un usuario con esas credenciales'}, status=status.HTTP_400_BAD_REQUEST)
        
        # en caso que no envien el token desde el front
        except: 
            return Response({'error': 'No se ha encontrado token en la peticion.'}, status=status.HTTP_409_CONFLICT)