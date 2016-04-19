from django.contrib import admin

# Register your models here.
from expdeploy.api.models import WorkerTask
from expdeploy.api.models import Metadata
from expdeploy.api.models import HistoryEvent

#register models


class WorkerTaskAdmin(admin.ModelAdmin):
	list_display = ["name", "wid"]
	class Meta:
		model = WorkerTask

class MetadataAdmin(admin.ModelAdmin):
	list_display = ["start", "end"]
	class Meta:
		model = Metadata

class HistoryAdmin(admin.ModelAdmin):
	list_display = ["newStatus"]
	class Meta:
		model = HistoryEvent

admin.site.register(HistoryEvent, HistoryAdmin)
admin.site.register(Metadata, MetadataAdmin)
admin.site.register(WorkerTask, WorkerTaskAdmin)