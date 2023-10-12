from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    
    # redefinimos el metodo create
    def create(self, validated_data):
        user = User(**validated_data)
        # utilizando el metodo set_password encriptamos la contaseña que pasamos en la validacioncde datos del post
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        updated_user = super().update(instance, validated_data)
        updated_user.set_password(validated_data['password'])
        updated_user.save()
        return updated_user


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

# el serializador UserSerializer pasa a JSON todos los campos pero con el metodo to_representation indicamos cuales pintar sobre la API.
    def to_representation(self, instance):
        return{
            'id': instance['id'],
            'username': instance['username'],
            'email': instance['email'],
            'password': instance['password']
        }