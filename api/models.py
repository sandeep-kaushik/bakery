from django.db import models
import re
# from jsonfield.fields import JSONField

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    def get_ingredients_ratio(self):
        # for item in self.ingredients_ratio:
        #
        # self.
        return 1


@receiver(post_save, sender=BakeryItem)
def update_bakery_item_sku(sender, instance, **kwargs):
    update_sku_post_save(sender, instance, prefix="SKU")



class IngredientsWeight(models.Model):
    weight = models.FloatField(null=True, blank=True, help_text="weight in grams")
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE, related_name='ingredient_ratios')
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE, related_name='ingredients_ratio')


class Inventory(models.Model):
    bakery_item = models.ForeignKey(BakeryItem, on_delete=models.CASCADE, related_name='bakery_item_inventory')
    manufacturing_date = models.DateField()
    expiry_date = models.DateField()
    quantity = models.IntegerField(default=0)


# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
#     login_id = models.ForeignKey(Customer_Login, on_delete=models.SET_NULL, blank=True, null=True)
#     no_of_products = models.PositiveSmallIntegerField()
#     address = models.ForeignKey(Address, on_delete=models.SET_NULL, blank=True, null=True)
#     order_price = models.PositiveIntegerField(null=True, blank=True)
#     rent_price = models.PositiveIntegerField(null=True, blank=True)
#     tax_price = models.PositiveIntegerField(null=True, blank=True)
#     discount_price = models.PositiveIntegerField(null=True, blank=True)
#     security_deposit = models.PositiveIntegerField(null=True, blank=True)
#     payment_request_id = models.CharField(max_length=50, null=True, blank=True)
#     payment_mode = models.CharField(max_length=8, null=True, blank=True)
#     payment_status = models.CharField(max_length=5, null=True, blank=True)
#     return_delivery = models.CharField(max_length=5, null=True, blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     guidelines = models.TextField(default='')
#     timeslot = models.CharField(max_length=50, default='')
#     discount_code = models.CharField(max_length=20, default='')
#     cancel = models.BooleanField(default=False)
#
#     def __unicode__(self):
#         return str(self.id) + str(self.customer) + " " + str(self.timestamp)
