# forms.py
from django import forms
from multiupload.fields import MultiFileField

class UploadForm(forms.Form):
	username = forms.CharField(man_length=120, blank=True, null=True)
    attachments = MultiFileField(max_num=10, max_file_size=1024*1024*5)