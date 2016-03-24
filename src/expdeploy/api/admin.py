from django.contrib import admin

# Register your models here.
from expdeploy.api.models import WorkerTask

#register models


class WorkerTaskAdmin(admin.ModelAdmin):
	list_display = ["name", "wid"]
	class Meta:
		model = WorkerTask

admin.site.register(WorkerTask, WorkerTaskAdmin)