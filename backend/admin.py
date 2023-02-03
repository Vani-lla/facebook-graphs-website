from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(JsonFile)
admin.site.register(Person)
admin.site.register(Messages)