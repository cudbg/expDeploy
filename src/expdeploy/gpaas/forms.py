# forms.py
from django import forms
from multiupload.fields import MultiFileField
from .models import ExperimentFile


class ExperimentForm(forms.Form):
	experiment = forms.CharField(max_length=120, required=True)
	hit_description = forms.CharField(max_length=120, required=True)
	#hit_payment = forms.FloatField(required=True)
	per_task_payment = forms.FloatField(required=True, min_value = 0.01)
	bonus_payment = forms.FloatField(required=True, min_value = 0)
	hit_keywords = forms.CharField(max_length=120, required=True)
	sandbox = forms.BooleanField(required=True)
	number_of_hits = forms.IntegerField(required=True);
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-3"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div></div>',
			error_row = u'%s',
			row_ender = '</p>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class HitDescriptionForm(forms.Form):
	hit_description = forms.CharField(max_length=120, required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class HitPaymentForm(forms.Form):
	#hit_payment = forms.FloatField(required=True)
	per_task_payment = forms.FloatField(required=True, min_value = 0.01)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s <b>(USD)</b> </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class BonusPaymentForm(forms.Form):
	bonus_payment = forms.FloatField(required=True, min_value = 0)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s <b>(USD)</b> </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class HitKeywordsForm(forms.Form):
	hit_keywords = forms.CharField(max_length=120, required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class SandboxForm(forms.Form):
	sandbox = forms.BooleanField(required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class TaskNumberForm(forms.Form):
	number_of_hits = forms.IntegerField(required=True);
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class UploadForm(forms.Form):
	attachments = MultiFileField(min_num = 1, max_num=50, max_file_size=1024*1024*5)
	class Meta:
		model = ExperimentFile

	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<p%(html_class_attr)s>%(label)s</p> &nbsp &nbsp &nbsp &nbsp %(field)s%(help_text)s<br></br>',
			error_row = u'%s',
			row_ender = '</p>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class UserForm(forms.Form): 
	accountname = forms.CharField(max_length=120)
	email = forms.EmailField(max_length=254) 
	key_id = forms.CharField(max_length=254) 
	secret_key = forms.CharField(max_length=254)
	password = forms.CharField(widget=forms.PasswordInput())
	#reenter_password =forms.CharField(widget=forms.PasswordInput())
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-3"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div></div>',
			error_row = u'%s',
			row_ender = '</p>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=120)
	password = forms.CharField(widget=forms.PasswordInput())
	
	