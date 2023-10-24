from django.contrib.sessions.models import Session

from datetime import datetime

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from apps.users.api.serializers import UserTokenSerializer

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
            else:
                return Response({'error': 'Este usuario no puede iniciar sesion.'}, status= status.HTTP_401_UNAUTHORIZED)
        else:
                return Response({'error': 'Nombre de usuario o contraseña incorrectos.'}, status= status.HTTP_400_BAD_REQUEST)
        return Response({'mensaje': 'Hola desde response'}, status=status.HTTP_200_OK)