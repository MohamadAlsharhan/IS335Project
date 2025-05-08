from rest_framework import viewsets
from django.db import transaction
from django.utils import timezone
from django.shortcuts import get_object_or_404  
from .models import RideRequest, Driver, Location, Pricing, Ride
from .serializers import RideRequestSerializer, RideSerializer
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from math import radians, sin, cos, sqrt, atan2
from django.shortcuts import render, redirect


class RideRequestViewSet(viewsets.ModelViewSet):
    queryset = RideRequest.objects.all()
    serializer_class = RideRequestSerializer

    @transaction.atomic
    @action(detail=True, methods=['put'])
    def accept_ride(self, request, pk=None):
        ride_request = self.get_object()

        if ride_request.status != "pending":
            return Response({"error": "Ride already accepted"}, status=400)

        ride_request.status = "accepted"
        ride_request.save()
        return Response({"success": "Ride accepted"})

def calculate_fare(vehicle_category, distance, is_surge_area):
    pricing = get_object_or_404(Pricing, vehicle_category=vehicle_category)  # ✅ Prevents errors
    surge_multiplier = pricing.surge_multiplier if is_surge_area else 1.0
    estimated_fare = pricing.base_rate * surge_multiplier * (distance / 40)  # Assuming speed = 40 km/h
    return estimated_fare

class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()  # ✅ Combined all functions into one class
    serializer_class = RideSerializer

    @action(detail=True, methods=['put'])
    def cancel_ride(self, request, pk=None):
        ride = self.get_object()
        if ride.status in ["completed", "cancelled"]:
            return Response({"error": "Cannot cancel this ride"}, status=400)

        ride.status = "cancelled"
        ride.save()
        return Response({"success": "Ride cancelled"})

    @action(detail=True, methods=['put'])
    def update_status(self, request, pk=None):
        ride = self.get_object()
        new_status = request.data.get("status")

        if new_status not in ["in_progress", "completed"]:
            return Response({"error": "Invalid status update"}, status=400)

        ride.status = new_status
        ride.save()
        return Response({"success": f"Ride status updated to {new_status}"})

    @action(detail=True, methods=['put'])
    def complete_ride(self, request, pk=None):
        ride = self.get_object()
        ride.status = "completed"
        ride.end_time = timezone.now()
        ride.distance_traveled = request.data.get("distance_traveled", 0)  # ✅ Prevents None errors
        ride.route_taken = request.data.get("route_taken", "Not provided")  # ✅ Default value
        ride.save()
        return Response({"success": "Ride completed", "distance": ride.distance_traveled})

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # Earth's radius in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c  # Distance in meters

@api_view(["GET"])
def find_nearby_drivers(request):
    pickup_lat = float(request.GET.get("latitude", 0))  # ✅ Prevents missing values
    pickup_long = float(request.GET.get("longitude", 0))

    drivers = Driver.objects.filter(status="online")
    nearby_drivers = []

    for driver in drivers:
        driver_location = driver.location
        distance = haversine(pickup_lat, pickup_long, driver_location.latitude, driver_location.longitude)
        if distance <= 5000:  # Limit to 5km radius
            nearby_drivers.append({"id": driver.id, "name": driver.name, "distance": distance})

    nearby_drivers.sort(key=lambda x: x["distance"])
    return Response({"drivers": nearby_drivers})

