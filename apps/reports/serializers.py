# apps/reports/serializers.py
from rest_framework import serializers
from .models import SavedReport

class SavedReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedReport
        fields = ['id', 'name', 'report_type', 'format', 'parameters', 'created_at', 'file']
        read_only_fields = ['created_at', 'file']