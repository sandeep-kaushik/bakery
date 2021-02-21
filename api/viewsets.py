from django.forms import model_to_dict
from rest_framework.viewsets import ModelViewSet
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated

from api.serializers import IngredientsSerializer, BakeryItemSerializer, InventoryPostSerializer, \
    InventoryGetSerializer, OrderSerializer
# from base.permissions import Isauthenticatedstaff
from api.models import Inventory, Ingredients, BakeryItem, IngredientsWeight, Order
from django.utils.timezone import datetime
from rest_framework.response import Response


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


class InventoryViewset(ModelViewSet):
    serializer_class = InventoryPostSerializer
    queryset = Inventory.objects.all()

    def list(self, request, *args, **kwargs):
        depth = self.request.query_params.get('depth', "")

        if depth != "" and depth != "null":
            self.serializer_class = InventoryGetSerializer
        else:
            self.serializer_class = InventoryPostSerializer

        return super(InventoryViewset, self).list(request, *args, **kwargs)


class OrderViewset(ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    # def get_queryset(self):
    #     super(OrderViewset, self).get_queryset()