# -*- coding: utf-8 -*-
from django import forms
from multiupload.fields import MultiFileField

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select your experiment HTML file');
    
class AttachmentForm(forms.Form):
    attachments = MultiFileField(min_num=1, max_num=3, max_file_size=1042*1042*5)

