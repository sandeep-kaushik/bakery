from rest_framework.viewsets import ModelViewSet
from accounts.serializers import RegistrationSerializer
from accounts.models import User


class RegistrationViewset(ModelViewSet):
    serializer_class = RegistrationSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = CuboidFilter

    queryset = User.objects.all()