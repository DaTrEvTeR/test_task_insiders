from django.urls import path, include
from rest_framework.routers import SimpleRouter
from rest_framework_nested.routers import NestedSimpleRouter
from .views import LocationViewSet, ReviewViewSet, LikeViewSet

# Обычный роутер для списка локаций
router = SimpleRouter()
router.register("locations", LocationViewSet, basename="locations")

# Вложенные роутеры для отзывов и лайков
locations_router = NestedSimpleRouter(router, "locations", lookup="location")
locations_router.register("reviews", ReviewViewSet, basename="location-reviews")
locations_router.register("likes", LikeViewSet, basename="location-likes")

urlpatterns = [
    path("", include(router.urls)),  # api/v1/locations/
    path("", include(locations_router.urls)),  # api/v1/locations/{id}/reviews/ и likes/
]
