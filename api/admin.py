from django.contrib import admin
from api.models import BakeryItem, Inventory, Ingredients, IngredientsWeight, Order


# Register your models here.


@admin.register(BakeryItem)
class BakeryItemAdmin(admin.ModelAdmin):
    pass


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Ingredients)
class IngredientsAdmin(admin.ModelAdmin):
    pass


@admin.register(IngredientsWeight)
class IngredientsWeightAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass