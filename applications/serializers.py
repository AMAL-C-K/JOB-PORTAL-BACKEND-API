from rest_framework import serializers
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    
    candidate = serializers.ReadOnlyField(source = 'candidate.username')
    job = serializers.ReadOnlyField(source='job.id')
    
    class Meta:
        model = Application
        fields = ['id', 'cover_letter', 'resume', 'status', 'applied_at']
        read_only_fields = ['status', 'applied_at']

class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = ['status']
