from django.contrib import admin
from .models import InferenceRequest


@admin.register(InferenceRequest)
class InferenceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'confidence_threshold', 'created_at')
    list_filter = ('created_at', 'confidence_threshold')
    search_fields = ('user__username',)
    readonly_fields = ('detections', 'created_at', 'updated_at')
