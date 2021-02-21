from django.contrib import admin
from .models import BakeryItem, Inventory, Ingredients, IngredientsWeight

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