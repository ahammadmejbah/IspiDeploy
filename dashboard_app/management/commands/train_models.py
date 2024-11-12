# dashboard_app/management/commands/train_models.py

import os
import pandas as pd
from django.core.management.base import BaseCommand
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from dashboard_app.models import ModelPerformance  # Import the ModelPerformance model

# Ensure that Django settings are configured
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'my_django_project.settings')  # Replace with your project name
import django
django.setup()

class Command(BaseCommand):
    help = 'Train a robust regression model with comprehensive preprocessing and save it as a .pkl file'

    def handle(self, *args, **kwargs):
        # Load the dataset (replace with your dataset path)
        dataset_path = 'Datasets/Ispahani.csv'  # Replace with the actual path to your dataset
        if not os.path.exists(dataset_path):
            self.stderr.write(self.style.ERROR(f"Dataset not found at {dataset_path}"))
            return

        df = pd.read_csv(dataset_path)

        # Specify the target column and feature columns
        target_column = 'Monthly Revenue'  # Target variable for regression
        feature_columns = [
            'Category', 'Flavor', 'Pack Type', 'Price/Unit', 'Total Weight/Carton',
            'Shelf Life', 'Calories/Unit', 'Protein (g)', 'Fat (g)', 'Carbs (g)'
        ]

        # Identify numerical and categorical features
        numeric_features = ['Price/Unit', 'Total Weight/Carton', 'Shelf Life', 'Calories/Unit', 'Protein (g)', 'Fat (g)', 'Carbs (g)']
        categorical_features = ['Category', 'Flavor', 'Pack Type']

        # Drop rows with missing target values
        df = df.dropna(subset=[target_column])

        # Impute missing values for numerical columns with the median and categorical columns with the mode
        df[numeric_features] = df[numeric_features].fillna(df[numeric_features].median())
        df[categorical_features] = df[categorical_features].apply(lambda x: x.fillna(x.mode()[0]))

        # Remove outliers using the IQR method for numerical features
        Q1 = df[numeric_features].quantile(0.25)
        Q3 = df[numeric_features].quantile(0.75)
        IQR = Q3 - Q1
        df = df[~((df[numeric_features] < (Q1 - 1.5 * IQR)) | (df[numeric_features] > (Q3 + 1.5 * IQR))).any(axis=1)]

        # Split the dataset into features (X) and target (y)
        X = df[feature_columns]
        y = df[target_column]

        # Create a column transformer for robust preprocessing
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', Pipeline([
                    ('scaler', MinMaxScaler()),
                    ('poly', PolynomialFeatures(degree=2, include_bias=False))
                ]), numeric_features),
                ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
            ]
        )

        # Define the model
        model = GradientBoostingRegressor(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)

        # Create a pipeline for the model
        model_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('regressor', model)])

        try:
            # Cross-validate the model for reliable performance metrics
            self.stdout.write("Performing cross-validation...")
            scores = cross_val_score(model_pipeline, X, y, cv=5, scoring='r2')
            mean_score = scores.mean()
            std_score = scores.std()
            self.stdout.write(self.style.SUCCESS(f"GradientBoostingRegressor Cross-Validation R² Score: {mean_score:.2f} ± {std_score:.2f}"))

            # Train the model on the full dataset
            self.stdout.write("Training the model on the full dataset...")
            model_pipeline.fit(X, y)

            # Make predictions on the full dataset (for demonstration; ideally, use a separate test set)
            y_pred = model_pipeline.predict(X)

            # Calculate metrics
            mse = mean_squared_error(y, y_pred)
            r2 = r2_score(y, y_pred)

            # Calculate Accuracy within Tolerance (e.g., within 10% of the actual value)
            tolerance = 0.10  # 10%
            correct_predictions = ((y_pred >= y * (1 - tolerance)) & (y_pred <= y * (1 + tolerance))).sum()
            total_predictions = len(y)
            accuracy_within_tolerance = (correct_predictions / total_predictions) * 100

            self.stdout.write(self.style.SUCCESS(f"GradientBoostingRegressor MSE: {mse:.2f}"))
            self.stdout.write(self.style.SUCCESS(f"GradientBoostingRegressor R² Score: {r2:.2f}"))
            self.stdout.write(self.style.SUCCESS(f"GradientBoostingRegressor Accuracy within ±{int(tolerance*100)}%: {accuracy_within_tolerance:.2f}%"))

            # Save the trained model as a .pkl file
            model_save_path = 'dashboard_app/saved_models/'
            os.makedirs(model_save_path, exist_ok=True)
            model_filename = os.path.join(model_save_path, 'GradientBoostingRegressor.pkl')
            joblib.dump(model_pipeline, model_filename)
            self.stdout.write(self.style.SUCCESS(f"Model saved as {model_filename}"))

            # Save the performance metrics to the database
            ModelPerformance.objects.create(
                model_name='GradientBoostingRegressor',
                mse=mse,
                r2_score=r2,
                cross_val_r2_mean=mean_score,
                cross_val_r2_std=std_score,
                accuracy_within_tolerance=accuracy_within_tolerance
            )
            self.stdout.write(self.style.SUCCESS("Model performance metrics saved to the database."))

        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error training GradientBoostingRegressor: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("Model training and saving process completed successfully."))
