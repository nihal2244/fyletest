from django.contrib import admin
from .models import Banks,Branches
# Register your models here.

myModels = [Banks,Branches]  # iterable list
admin.site.register(myModels)
