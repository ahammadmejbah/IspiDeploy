# dashboard_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('total-revenue/', views.total_revenue_detail, name='total_revenue_detail'),
    path('top-selling/', views.top_selling_product, name='top_selling_product'),
    path('category-analysis/', views.category_analysis_detail, name='category_analysis_detail'),
    path('monthly-sales/', views.monthly_sales_detail, name='monthly_sales_detail'),
    path('profit-margin/', views.profit_margin_detail, name='profit_margin_detail'),
    path('shelf-life/', views.shelf_life_detail, name='shelf_life_detail'),
    path('sales-growth/', views.sales_growth_detail, name='sales_growth_detail'),
    path('revenue-flavor/', views.revenue_flavor_detail, name='revenue_flavor_detail'),
    path('revenue-packaging/', views.revenue_packaging_detail, name='revenue_packaging_detail'),
    path('machine-learning-models/', views.machine_learning_models_detail, name='machine_learning_models_detail'),
    path('model-performance/', views.model_performance, name='model_performance'),
]
