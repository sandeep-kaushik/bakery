from django.forms import model_to_dict
from rest_framework import serializers
from api.models import Ingredients, Inventory, BakeryItem, IngredientsWeight


class IngredientsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredients
        fields = '__all__'


class IngredientsWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = IngredientsWeight
        exclude =("bakery_item",)


class BakeryItemSerializer(serializers.ModelSerializer):

    ingredients_weight_list = IngredientsWeightSerializer(many=True, required=False)

    class Meta:
        model = BakeryItem
        fields = ('ingredients_weight_list', "name", 'description',
                  'Item_count_in_package', 'measurement_type', 'weight', 'type', 'price')

    def to_representation(self, instance):
        returned_json = super(
            BakeryItemSerializer, self).to_representation(instance)
        ingredients_weight_list= []
        try:
            ingredients_weight_data = IngredientsWeight.objects.filter(bakery_item__id=instance.id)
            for ingredient_item in ingredients_weight_data:
                data = model_to_dict(ingredient_item, exclude=('bakery_item', ))
                ingredients_weight_list.append(data)
            returned_json['ingredients_weight_list'] = ingredients_weight_list
        except:
            print('IngredientsWeight with instance id {} does not exist'.format(
                instance.id))
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