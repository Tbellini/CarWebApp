from django.contrib import admin
from .models import User, Car, CarBooked
# Register your models here.




class CarAdmin(admin.ModelAdmin):
    pass
admin.site.register(Car,CarAdmin)

class CarBookedAdmin(admin.ModelAdmin):
    pass
admin.site.register(CarBooked,CarBookedAdmin)
