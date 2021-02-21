from rest_framework.viewsets import ModelViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from api.serializers import IngredientsSerializer, BakeryItemSerializer
# from base.permissions import Isauthenticatedstaff
from api.models import Inventory, Ingredients, BakeryItem


class IngredientsViewset(ModelViewSet):
    serializer_class = IngredientsSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = CuboidFilter

    queryset = Ingredients.objects.all()

    # def get_permissions(self):
    #     if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
    #         self.permission_classes = [Isauthenticatedstaff]
    #     else:
    #         self.permission_classes = [IsAuthenticated]
    #     return super(CuboidViewset, self).get_permissions()


class BakeryItemViewset(ModelViewSet):
    serializer_class = BakeryItemSerializer
    queryset = BakeryItem.objects.all()
