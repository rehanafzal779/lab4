from rest_framework import serializers
from .models import InferenceRequest


class InferenceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = InferenceRequest
        fields = ['id', 'image', 'result_image', 'detections', 'confidence_threshold', 'created_at']
        read_only_fields = ['id', 'result_image', 'detections', 'created_at']
