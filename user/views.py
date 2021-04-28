from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import User
from user.permissions import IsAccountOwner
from user.serializers import UserModelSerializer, UserSignUpSerializer,\
    UserLoginSerializer, UserChangePasswordSerializer


class UserViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """Registrar, Login y Obtener usuario"""

    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    lookup_field = "username"

    def get_object(self):
        return self.request.user

    def get_permissions(self):
        if self.action in ['register', 'login', ]:
            permissions = [AllowAny]

        elif self.action in ['detail', 'update', 'partial_update','profile']:
            permissions = [IsAuthenticated, IsAccountOwner, ]

        else:
            permissions = [IsAuthenticated, ]

        return [p() for p in permissions]

    @action(detail=False, methods=['POST'])
    def register(self, request):
        """Registrar un nuevo usuario"""
        serializer = UserSignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data

        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):
        """Iniciar sesión"""
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['GET'])
    def profile(self, request, *args, **kwargs):
        """Obtiene el perfil del usuario, necesita estar autenticado"""
        user = self.get_object()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['PATCH'])
    def soft_delete(self, request, *args, **kwargs):
        """Elimina un usuario, necesita estar autenticado"""
        instance = request.user
        if instance is not None:
            instance.is_active = False
            instance.save()
            data = UserModelSerializer(instance).data
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['PATCH'])
    def change_password(self, request, *args, **kwargs):
        """
        Cambia la contraseña del usuario,
        necesita proporcionar la contraseña antigua
        Código sacado de:
        https://www.edureka.co/community/74056/how-to-update-user-password-in-django-rest-framework
        """
        serializer = UserChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not request.user.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Contraseña incorrecta."]},
                            status=status.HTTP_400_BAD_REQUEST)

        request.user.set_password(serializer.data.get("new_password"))
        request.user.save()

        return Response({'message': 'Contraseña actualizada correctamente'},
                        status=status.HTTP_200_OK)
