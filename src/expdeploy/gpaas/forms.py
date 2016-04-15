# forms.py
from django import forms
from multiupload.fields import MultiFileField
from .models import ExperimentFile


class ExperimentForm(forms.Form):
	experiment = forms.CharField(max_length=120, required=True)
	hit_description = forms.CharField(max_length=120, required=True)
	hit_payment = forms.FloatField(required=True)
	hit_keywords = forms.CharField(max_length=120, required=True)
	sandbox = forms.BooleanField(required=True)
	number_of_hits = forms.IntegerField(required=True);

class HitDescriptionForm(forms.Form):
	hit_description = forms.CharField(max_length=120, required=True)

class HitPaymentForm(forms.Form):
	hit_payment = forms.FloatField(required=True)

class HitKeywordsForm(forms.Form):
	hit_keywords = forms.CharField(max_length=120, required=True)

class SandboxForm(forms.Form):
	sandbox = forms.BooleanField(required=True)

class TaskNumberForm(forms.Form):
	number_of_hits = forms.IntegerField(required=True);

class UploadForm(forms.Form):
	attachments = MultiFileField(min_num = 1, max_num=10, max_file_size=1024*1024*5)
	class Meta:
		model = ExperimentFile

class UserForm(forms.Form): 
	accountname = forms.CharField(max_length=120)
	email = forms.EmailField(max_length=254) 
	key_id = forms.CharField(max_length=254) 
	secret_key = forms.CharField(max_length=254)
	password = forms.CharField(widget=forms.PasswordInput())
	#reenter_password =forms.CharField(widget=forms.PasswordInput())

class LoginForm(forms.Form):
	username = forms.CharField(max_length=120)
	password = forms.CharField(widget=forms.PasswordInput())
	
	