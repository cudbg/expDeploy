# -*- coding: utf-8 -*-
from django.contrib import admin
from expdeploy.gpaas.models import ExperimentFile
from expdeploy.gpaas.models import ExperimentModel
from expdeploy.gpaas.models import Researcher

#register models

class FileAdmin(admin.ModelAdmin):
	list_display = ["docfile", "username"]
	class Meta:
		model = ExperimentFile

class ExperimentAdmin(admin.ModelAdmin):
	list_display = ["name", "username"]
	class Meta:
		model = ExperimentModel


class ResearcherAdmin(admin.ModelAdmin):
	list_display = ["aws_key_id", "aws_secret_key","user"]
	class Meta:
		model = ExperimentModel


admin.site.register(ExperimentFile, FileAdmin)
admin.site.register(ExperimentModel, ExperimentAdmin)
admin.site.register(Researcher, ResearcherAdmin)