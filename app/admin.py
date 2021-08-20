from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
class Registationadmin(admin.ModelAdmin):
	list_display=["name","lname","email","password"]
	list_filter=("lname",)
	search_fields=("lname__startswith",)
admin.site.register(Registation,Registationadmin)
