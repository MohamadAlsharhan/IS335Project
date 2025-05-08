from django.db import models

class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

class Rider(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)

class Driver(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=255)
    vehicle_make = models.CharField(max_length=255)
    vehicle_model = models.CharField(max_length=255)
    vehicle_color = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=20)
    driver_license = models.CharField(max_length=255)
    status = models.CharField(
        max_length=50,
        choices=[
            ("online", "Online"),
            ("busy", "Busy"),
            ("offline", "Offline"),
            ("suspended", "Suspended"),
        ],
    )

class Vehicle(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE)
    category = models.CharField(
        max_length=50,
        choices=[
            ("economy", "Economy"),
            ("premium", "Premium"),
            ("family", "Family"),
        ],
    )
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)

class RideRequest(models.Model):
    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pickup_requests")
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="dropoff_requests")
    status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("accepted", "Accepted"),
            ("cancelled", "Cancelled"),
        ],
    )

class Ride(models.Model):
    STATUS_CHOICES = [
        ("requested", "Requested"),
        ("accepted", "Accepted"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    rider = models.ForeignKey(Rider, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="pickup_rides")  
    dropoff_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="dropoff_rides")  
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    distance_traveled = models.FloatField(null=True, blank=True)
    route_taken = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)  

class Pricing(models.Model):
    vehicle_category = models.CharField(
        max_length=50,
        choices=[
            ("economy", "Economy"),
            ("premium", "Premium"),
            ("family", "Family"),
        ],
    )
    base_rate = models.DecimalField(max_digits=10, decimal_places=2)
    surge_multiplier = models.FloatField(default=1.0)