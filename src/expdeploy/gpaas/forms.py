# forms.py
from django import forms
from multiupload.fields import MultiFileField


class UploadForm(forms.Form):
	attachments = MultiFileField(min_num = 1, max_num=10, max_file_size=1024*1024*5)
	experiment = forms.CharField(max_length=120, required=True)

class UserForm(forms.Form): 
	accountname = forms.CharField(max_length=120)
	email = forms.EmailField(max_length=254) 
	key_id = forms.CharField(max_length=254) 
	password = forms.CharField(widget=forms.PasswordInput())
	secret_key = forms.CharField(max_length=254)
	#reenter_password =forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput())
	username = forms.CharField(max_length=120)
	