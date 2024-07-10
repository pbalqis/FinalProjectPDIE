from django.contrib import admin
from . models import Employee, Leave, Dashboard, Package

# Register your models here.

admin.site.register(Employee)
admin.site.register(Leave)
admin.site.register(Dashboard)
admin.site.register(Package)