from django.db.models import F
from django.forms import model_to_dict
from rest_framework import serializers
import logging
from django.core.exceptions import ValidationError

from api.models import Ingredients, Inventory, BakeryItem, IngredientsWeight, Order, OrderItems

logger = logging.getLogger(__name__)


class IngredientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredients
        fields = '__all__'


class IngredientsWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsWeight
        exclude = ("bakery_item",)


class BakeryItemSerializer(serializers.ModelSerializer):
    ingredients_weight_list = IngredientsWeightSerializer(many=True, required=False)

    class Meta:
        model = BakeryItem
        fields = ('ingredients_weight_list', "name", 'description',
                  'Item_count_in_package', 'measurement_type', 'weight', 'type', 'price')

    def to_representation(self, instance):
        returned_json = super(
            BakeryItemSerializer, self).to_representation(instance)
        try:
            ingredients_total_weight = instance.get_ingredients_total_weight
            ingredients_weight_data = instance.ingredients_ratio.all().annotate(
                percentage=(F('weight') / ingredients_total_weight) * 100).values('id', 'weight','percentage', 'ingredient')
            returned_json['ingredients_weight_list'] = list(ingredients_weight_data)
        except Exception as e:
            logger.error('IngredientsWeight with instance id %s exited with error %s'%
                (instance.id, e))
        return returned_json

    def create(self, validated_data):
        ingredients_weight_list = validated_data.pop("ingredients_weight_list", None)
        bakery_item_obj = BakeryItem(**validated_data)
        bakery_item_obj.save()
        if ingredients_weight_list:
            for item in ingredients_weight_list:
                ingredients_weight_obj = IngredientsWeight(**item)
                ingredients_weight_obj.bakery_item = bakery_item_obj
                ingredients_weight_obj.save()
        return bakery_item_obj


class InventoryPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = "__all__"
        depth = 2


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItems
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    bakery_items = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = ('customer', 'bakery_items', 'payment_mode', 'guidelines')

    def create(self, validated_data):
        bakery_items = validated_data.pop('bakery_items')
        no_of_bakery_item = len(bakery_items)
        validated_data['no_of_bakery_item'] = no_of_bakery_item

        try:
            validated_data['order_price'] = 0
            order = Order.objects.create(**validated_data)

            if bakery_items:
                for item in bakery_items:
                    try:
                        validated_data['order_price']+= item['bakery_item'].price

                        order_item = OrderItems(order=order, quantity=item['quantity'], bakery_item=item['bakery_item'])

                        order_item.save()
                    except Exception as e:
                        pass
            order.order_price = validated_data['order_price']
            order.save()
            return order
        except Exception as e:
            logger.error(
                "Unable to create Order in order Create api with Order data provided as %s \
               and bakery_items %s and the exception occured is ::: %s" %
                (validated_data, bakery_items, e))

    def validate_bakery_items(self, value):

        for item in value:
            inventory_obj = item['bakery_item'].bakery_item_inventory
            if inventory_obj.quantity - item['quantity'] < 0:
                raise ValidationError("stock for bakery_item {} is not available with requested quantity".format(
                    item['bakery_item'].id))

        return value