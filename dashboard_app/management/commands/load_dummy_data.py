# dashboard_app/management/commands/load_dummy_data.py

import json
import os
from django.core.management.base import BaseCommand
from dashboard_app.models import ModelPerformance
from django.utils.dateparse import parse_datetime
from django.conf import settings

class Command(BaseCommand):
    help = 'Load dummy model performance data from JSON file'

    def handle(self, *args, **kwargs):
        """
        Entry point for the management command.
        Loads data from 'model_performance_data.json' and populates the ModelPerformance model.
        """
        # Define the path to the JSON file
        # Assuming the JSON file is located at dashboard_app/data/model_performance_data.json
        json_file_path = os.path.join(
            settings.BASE_DIR,  # Base directory of the Django project
            'dashboard_app',
            'data',
            'model_performance_data.json'
        )

        # Check if the JSON file exists
        if not os.path.exists(json_file_path):
            self.stderr.write(self.style.ERROR(f"JSON file not found at {json_file_path}"))
            return

        try:
            # Open and load the JSON data
            with open(json_file_path, 'r') as file:
                data = json.load(file)
                self.stdout.write(self.style.SUCCESS(f"Successfully loaded data from {json_file_path}"))
        except json.JSONDecodeError as e:
            self.stderr.write(self.style.ERROR(f"JSON decode error: {str(e)}"))
            return
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error reading JSON file: {str(e)}"))
            return

        # Iterate through each entry in the JSON data
        for entry in data:
            try:
                # Extract and validate each field
                model_name = entry.get('model_name')
                mse = float(entry.get('mse', 0))
                r2_score = float(entry.get('r2_score', 0))
                cross_val_r2_mean = float(entry.get('cross_val_r2_mean', 0))
                cross_val_r2_std = float(entry.get('cross_val_r2_std', 0))
                accuracy_within_tolerance = float(entry.get('accuracy_within_tolerance', 0))
                trained_at_str = entry.get('trained_at')

                # Parse the 'trained_at' datetime string
                trained_at = parse_datetime(trained_at_str)
                if trained_at is None:
                    self.stderr.write(self.style.WARNING(
                        f"Invalid datetime format for model '{model_name}': '{trained_at_str}'. Skipping entry."
                    ))
                    continue

                # Create or update the ModelPerformance entry
                obj, created = ModelPerformance.objects.update_or_create(
                    model_name=model_name,
                    defaults={
                        'mse': mse,
                        'r2_score': r2_score,
                        'cross_val_r2_mean': cross_val_r2_mean,
                        'cross_val_r2_std': cross_val_r2_std,
                        'accuracy_within_tolerance': accuracy_within_tolerance,
                        'trained_at': trained_at
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Created ModelPerformance for '{model_name}'"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"Updated ModelPerformance for '{model_name}'"))

            except Exception as e:
                self.stderr.write(self.style.ERROR(
                    f"Error processing model '{entry.get('model_name', 'Unknown')}': {str(e)}"
                ))
                continue

        self.stdout.write(self.style.SUCCESS("All dummy data loaded successfully."))
