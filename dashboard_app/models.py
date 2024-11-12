# dashboard_app/models.py

from django.db import models

class ModelPerformance(models.Model):
    model_name = models.CharField(max_length=100)
    mse = models.FloatField()
    r2_score = models.FloatField()
    cross_val_r2_mean = models.FloatField()
    cross_val_r2_std = models.FloatField()
    accuracy_within_tolerance = models.FloatField(null=True, blank=True)  # New field
    trained_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_name} - {self.trained_at.strftime('%Y-%m-%d %H:%M')}"
