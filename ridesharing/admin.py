from django.contrib import admin
from .models import Location, Rider, Driver, Vehicle, RideRequest, Ride, Pricing

'''
 Superuser information:
 Username: mm
 Password: 123123
'''

admin.site.register(Location)
admin.site.register(Rider)
admin.site.register(Driver)
admin.site.register(Vehicle)
admin.site.register(RideRequest)
admin.site.register(Ride)
admin.site.register(Pricing)