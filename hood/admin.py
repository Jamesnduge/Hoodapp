from django.contrib import admin
from django.forms.widgets import TextInput
from .models import Hood, Bio, Business, Status


admin.site.register(Hood)
admin.site.register(Bio)
admin.site.register(Business)
admin.site.register(Status)