from rest_framework.routers import DefaultRouter
from api.viewsets import IngredientsViewset, BakeryItemViewset
from accounts.viewsets import RegistrationViewset

router = DefaultRouter()

router.register('ingredents', IngredientsViewset)
router.register('bakeryitem', BakeryItemViewset)
router.register('register', RegistrationViewset)

