# forms.py
from django import forms
from multiupload.fields import MultiFileField
from .models import ExperimentFile

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

class ExperimentForm(forms.Form):
	experiment = forms.CharField(max_length=120, required=True)
	hit_description = forms.CharField(max_length=120, required=True)
	per_task_payment = forms.FloatField(required=True, min_value = 0.01)
	task_submission_payment= forms.FloatField(required=True, min_value=0)
	bonus_payment = forms.FloatField(required=True, min_value = 0)
	hit_keywords = forms.CharField(max_length=120, required=True)
	number_of_assignments = forms.IntegerField(required=True)
	hit_duration_in_seconds = forms.IntegerField(required=False)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-3"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div></div>',
			error_row = u'%s',
			row_ender = '</p>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class ConfigFileForm(forms.Form):
	config_file_name = forms.CharField(required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-3"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class HitDescriptionForm(forms.Form):
	hit_description = forms.CharField(max_length=120, required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-3"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class HitDurationForm(forms.Form):
	hit_duration_in_seconds = forms.IntegerField(required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
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

class LoginForm(forms.Form):
	username = forms.CharField(max_length=120)
	password = forms.CharField(widget=forms.PasswordInput())

class QualificationsForm(forms.Form):
	us_residents_only = forms.BooleanField(required=False) # adults only
	percentage_hits_approved = forms.IntegerField(required=True)
	percentage_assignments_submitted = forms.IntegerField(required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="row" style="margin-top:5px"><div class="col-sm-5"> %(html_class_attr)s %(label)s</div> <div class="col-sm-4"> %(field)s%(help_text)s</div></div>',
			error_row = u'%s',
			row_ender = '</p>',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class TaskNumberForm(forms.Form):
	number_of_assignments = forms.IntegerField(required=True);
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
			error_row = u'%s',
			row_ender = '',
			help_text_html = u' <span class="helptext">%s</span>',
			errors_on_separate_row = True)

class TaskSubmissionPaymentForm(forms.Form):
	task_submission_payment = forms.FloatField(required=True)
	def as_p(self):
	#"Returns this form rendered as HTML <p>s."
		return self._html_output(
			normal_row = u'<div class="col-sm-3">%(html_class_attr)s %(label)s <b>(USD)</b> </div> <div class="col-sm-4"> %(field)s%(help_text)s</div>',
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