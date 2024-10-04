from django.contrib import admin

from .models import Breed, Kitten

admin.site.register(Kitten)
admin.site.register(Breed)
