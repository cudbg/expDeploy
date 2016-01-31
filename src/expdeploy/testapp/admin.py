# -*- coding: utf-8 -*-
from django.contrib import admin
from expdeploy.testapp.models import ExperimentFile

#register models

class FileAdmin(admin.ModelAdmin):
	list_display = ["docfile", "username"]
	class Meta:
		model = ExperimentFile

admin.site.register(ExperimentFile, FileAdmin)