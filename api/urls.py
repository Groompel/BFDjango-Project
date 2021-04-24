from django.db.models import base
from .views import CommercialProperyViewSet, FlatPropertyViewSet, HousePropertyViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('property/commercial', CommercialProperyViewSet,
                basename='commercial property')
router.register('property/house', HousePropertyViewSet,
                basename='house property')
router.register('property/flat', FlatPropertyViewSet, basename='flat property')

urlpatterns = router.urls
