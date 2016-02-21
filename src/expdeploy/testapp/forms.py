# forms.py
from django import forms
from multiupload.fields import MultiFileField

class UploadForm(forms.Form):
	username = forms.CharField(max_length=120)
	experiment = forms.CharField(max_length=120)
	attachments = MultiFileField(min_num = 1, max_num=10, max_file_size=1024*1024*5)


class UserForm(forms.Form):
	accountname = forms.CharField(max_length=120)
	email = forms.EmailField(max_length=254) #.edu restriction later
	password = forms.CharField(widget=forms.PasswordInput())

