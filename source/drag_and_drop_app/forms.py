from django import forms
from .models import UploadModel

class UploadInfoForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']