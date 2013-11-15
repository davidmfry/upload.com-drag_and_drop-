from django.contrib import admin
from .models import UploadModel, FileNameModel

class UploadFormAdmin(admin.ModelAdmin):
    class Meta:
        model = UploadModel
admin.site.register(UploadModel, UploadFormAdmin)


class FileNameAdmin(admin.ModelAdmin):
    class Meta:
        model = FileNameModel
admin.site.register(FileNameModel, FileNameAdmin)
    