from django.db import models
from django.db.models import Sum, F
import re
import logging

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User

logger = logging.getLogger(__name__)


def update_sku_post_save(sender_model, instance, prefix):
    """
    This function will update the SKU post save because code's suffix is primary key, which is generated post save.
    """

    if not instance.sku or instance.sku and not re.match(
            r"[A-Z]+[D,P][0-9]+", instance.sku):

        instance_sku = prefix + str(instance.pk)

        sender_model.objects.filter(id=instance.id).update(
            sku=instance_sku)


class Ingredients(models.Model):
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')


class BakeryItem(models.Model):
    item_type = ((1, "dry"),(2, 'wet'))
    measurement_type = ((1, "Weight"),(2, 'Packaging'))

    sku = models.SlugField(unique=True, blank=True)
    name = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    Item_count_in_package = models.IntegerField(null=True, blank=True)
    measurement_type = models.IntegerField(default=1, choices=measurement_type)
    weight = models.FloatField(null=True, blank=True, help_text="weight in grams")
    type = models.IntegerField(default=1, choices=item_type)
    price = models.FloatField(default=0.0)

    @property
    def get_ingredients_total_weight(self):
        """
            This function return the total weight of ingredients in an BakeryItem
        """

        ingredients_total_weight = BakeryItem.objects.annotate(
            ingredents_total_weight=Sum("ingredients_ratio__weight")).get(id=self.id).ingredents_total_weight
        return ingredients_total_weight


@receiver(post_save, sender=BakeryItem)
def update_bakery_item_sku(sender, instance, **kwargs):
    update_sku_post_save(sender, instance, prefix="SKU")


class IngredientsWeight(models.Model):
    weight = models.FloatField(null=True, blank=True, help_text="weight in grams")
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name='ingredient_ratios')
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE, related_name='ingredients_ratio')


class Inventory(models.Model):
    bakery_item = models.OneToOneField(BakeryItem, on_delete=models.CASCADE, related_name='bakery_item_inventory')
    quantity = models.IntegerField(default=0)


class Order(models.Model):
    pay_status = ((1, "Success"), (2, 'Failed'), (3, 'Pending'))

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    no_of_bakery_item = models.PositiveSmallIntegerField()
    order_price = models.PositiveIntegerField(null=True, blank=True)
    discount_price = models.PositiveIntegerField(null=True, blank=True)
    payment_mode = models.CharField(max_length=8, null=True, blank=True)
    payment_status = models.CharField(max_length=5, null=True, blank=True, choices=pay_status)
    return_delivery = models.CharField(max_length=5, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    guidelines = models.TextField(default='')
    cancel = models.BooleanField(default=False)

    def check_order(self):
        pass

    def place_order(self):
        pass

    def cancel_order(self):
        pass


class OrderItems(models.Model):
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE, related_name='bakery_item_order')
    quantity = models.IntegerField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")

    def update_inventory(self):

        """
        Update inventory after creating an order and is corresponding order items
        :return: None
        """

        try:
            inventory_obj = self.bakery_item.bakery_item_inventory
            inventory_obj.quantity -= self.quantity
            inventory_obj.save()
        except Exception as e:
            logger.error(
                "Unable to update inventory with order item id  %s' with error %s" %(self.id, e))


@receiver(post_save, sender=OrderItems)
def update_inventory_signal(sender, instance, **kwargs):
    """
    Post save signal for OrderItems to update inventory after saving the OrderItems

    :param sender:
    :param instance:
    :param kwargs:
    :return: None
    """
    instance.update_inventory()
