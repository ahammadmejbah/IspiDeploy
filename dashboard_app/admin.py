# dashboard_app/admin.py

from django.contrib import admin
from .models import ModelPerformance

@admin.register(ModelPerformance)
class ModelPerformanceAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'mse', 'r2_score', 'cross_val_r2_mean', 'cross_val_r2_std', 'accuracy_within_tolerance', 'trained_at')
    list_filter = ('model_name', 'trained_at')
    search_fields = ('model_name',)
