from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RideRequestViewSet, RideViewSet 



router = DefaultRouter()
router.register(r'ride_requests', RideRequestViewSet)
router.register(r'rides', RideViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('rides/<int:pk>/cancel/', RideViewSet.as_view({'put': 'cancel_ride'})),
    path('rides/<int:pk>/status/', RideViewSet.as_view({'put': 'update_status'})),
    path('rides/<int:pk>/complete/', RideViewSet.as_view({'put': 'complete_ride'})),
    
]