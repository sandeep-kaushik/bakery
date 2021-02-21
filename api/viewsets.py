from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, mixins
from api.permissions import Isauthenticatedstaff
from api.serializers import IngredientsSerializer, BakeryItemSerializer, InventoryPostSerializer, \
    InventoryGetSerializer, OrderSerializer
from api.models import Inventory, Ingredients, BakeryItem, IngredientsWeight, Order


class IngredientsViewset(ModelViewSet):
    serializer_class = IngredientsSerializer
    queryset = Ingredients.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [Isauthenticatedstaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(IngredientsViewset, self).get_permissions()


class BakeryItemViewset(ModelViewSet):
    serializer_class = BakeryItemSerializer
    queryset = BakeryItem.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [Isauthenticatedstaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(BakeryItemViewset, self).get_permissions()


class InventoryViewset(ModelViewSet):
    serializer_class = InventoryPostSerializer
    queryset = Inventory.objects.all()

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [Isauthenticatedstaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(InventoryViewset, self).get_permissions()

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

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE', 'PATCH']:
            self.permission_classes = [Isauthenticatedstaff]
        else:
            self.permission_classes = [IsAuthenticated]
        return super(OrderViewset, self).get_permissions()


class MyOrderViewset(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related('order_items')
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        self.queryset = self.get_queryset().filter(customer = request.user)
        return super(MyOrderViewset, self).list(request, *args, **kwargs)