from rest_framework.routers import DefaultRouter
from api.viewsets import IngredientsViewset, BakeryItemViewset, InventoryViewset, OrderViewset, MyOrderViewset
from accounts.viewsets import RegistrationViewset

router = DefaultRouter()

router.register('ingredents', IngredientsViewset)
router.register('bakeryitem', BakeryItemViewset)
router.register('inventory', InventoryViewset)
router.register('register', RegistrationViewset)
router.register('order', OrderViewset)
router.register('myorder', MyOrderViewset)

