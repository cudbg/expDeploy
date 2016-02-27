# -*- coding: utf-8 -*-
from django.contrib import admin
from expdeploy.testapp.models import ExperimentFile
from expdeploy.testapp.models import ExperimentModel

#register models

class FileAdmin(admin.ModelAdmin):
	list_display = ["docfile", "username"]
	class Meta:
		model = ExperimentFile

class ExperimentAdmin(admin.ModelAdmin):
	list_display = ["name", "username"]
	class Meta:
		model = ExperimentModel

admin.site.register(ExperimentFile, FileAdmin)
admin.site.register(ExperimentModel, ExperimentAdmin)