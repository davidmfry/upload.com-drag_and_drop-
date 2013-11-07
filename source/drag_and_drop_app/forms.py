from django import forms
from .models import UploadModel

class UploadInfoForm(forms.ModelForm):
    class Meta:
        model = UploadModel
        fields = ['first_name', 'last_name', 'email', 'phone', 'message']

class MasterResponseForm(forms.Form):

	user_id = forms.IntegerField()
	checked_by = forms.CharField(max_length=250)
	replay_message = forms.CharField(widget = forms.Textarea)