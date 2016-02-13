from __future__ import unicode_literals

# -*- coding: utf-8 -*-
from django.db import models
from uuid import uuid4
import os

#arbitrary name generating function
def uuid_file_name(instance, filename):
	instance.filename = filename
	filetype = filename.split('.')[-1]
	filename = "%s.%s" % (str(uuid4()), filetype)
	return os.path.join('testapp/webfiles/', filename)


class ExperimentFile(models.Model):
<<<<<<< HEAD
	#can send html and static files to separate locations later
    docfile = models.FileField(upload_to='testapp/webfiles')
    username = models.CharField(max_length=120, blank=True, null=True)
    filename = models.CharField(max_length=120, blank=True, null=True)
=======
	#original_filename stored as charfield.
	original_filename = models.CharField(max_length = 128)
	docfile = models.FileField(upload_to=uuid_file_name)
	username = models.CharField(max_length=120, blank=True, null=True)
	filetext = models.TextField()
>>>>>>> origin/master

	def __str__(self):
		return str(self.docfile)