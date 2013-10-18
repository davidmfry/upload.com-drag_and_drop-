from django.contrib import admin
from .models import UploadModel

class UploadFormAdmin(admin.ModelAdmin):
    class Meta:
        model = UploadModel
admin.site.register(UploadModel, UploadFormAdmin)
    