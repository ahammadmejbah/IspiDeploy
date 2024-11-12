# dashboard_app/views.py
from django.shortcuts import render
import pandas as pd
import plotly.express as px
from django.http import JsonResponse
import pandas as pd

def index(request):
    # Load the dataset (ensure the path is correct)
    df = pd.read_csv('Datasets/Ispahani.csv')
    
    # Calculate primitive values for each feature
    total_revenue = df['Monthly Revenue'].sum()
    top_product = df.groupby('Product Name')['Monthly Sales Volume (units)'].sum().idxmax()
    top_product_sales = df.groupby('Product Name')['Monthly Sales Volume (units)'].sum().max()
    top_category = df.groupby('Category')['Monthly Sales Volume (units)'].sum().idxmax()
    avg_monthly_sales = df['Monthly Sales Volume (units)'].mean()
    avg_profit_margin = df['Monthly Growth Rate'].mean()
    max_shelf_life_product = df.loc[df['Shelf Life'].idxmax(), 'Product Name']
    min_shelf_life_product = df.loc[df['Shelf Life'].idxmin(), 'Product Name']
    avg_growth_rate = df['Monthly Growth Rate'].mean()
    top_flavor_revenue = df.groupby('Flavor')['Monthly Revenue'].sum().idxmax()
    top_packaging_revenue = df.groupby('Pack Type')['Monthly Revenue'].sum().idxmax()

    # Context for the template
    context = {
        'total_revenue': total_revenue,
        'top_product': top_product,
        'top_product_sales': top_product_sales,
        'top_category': top_category,
        'avg_monthly_sales': avg_monthly_sales,
        'avg_profit_margin': avg_profit_margin,
        'max_shelf_life_product': max_shelf_life_product,
        'min_shelf_life_product': min_shelf_life_product,
        'avg_growth_rate': avg_growth_rate,
        'top_flavor_revenue': top_flavor_revenue,
        'top_packaging_revenue': top_packaging_revenue,
    }
    return render(request, 'dashboard_app/index.html', context)



# Load the dataset (ensure the path is correct)
df = pd.read_csv('Datasets/Ispahani.csv')


####################################


def total_revenue_detail(request):
    df = pd.read_csv('Datasets/Ispahani.csv')
    # Ensure necessary columns are numeric types, and handle non-numeric values gracefully
    df['Monthly Revenue'] = pd.to_numeric(df['Monthly Revenue'], errors='coerce')
    df['Monthly Sales Volume (units)'] = pd.to_numeric(df['Monthly Sales Volume (units)'], errors='coerce')
    df['Calories/Unit'] = pd.to_numeric(df['Calories/Unit'], errors='coerce')
    df['Price/Unit'] = pd.to_numeric(df['Price/Unit'], errors='coerce')

    # Drop rows with NaN values in critical columns to avoid plotting issues
    df = df.dropna(subset=['Monthly Revenue', 'Monthly Sales Volume (units)', 'Calories/Unit', 'Price/Unit'])

    # Plot 1: Line plot for total revenue over time
    line_fig = px.line(
        df,
        x='Sales Month',
        y='Monthly Revenue',
        title='Total Revenue Trend Over Time',
        labels={'Sales Month': 'Month', 'Monthly Revenue': 'Revenue ($)'}
    )
    line_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    line_plot_html = line_fig.to_html(full_html=False)

    # Plot 2: Bar plot for top 10 revenue-generating products
    top_products = df.groupby('Product Name')['Monthly Revenue'].sum().sort_values(ascending=False).head(10)
    bar_fig = px.bar(
        x=top_products.index,
        y=top_products.values,
        title='Top 10 Revenue-Generating Products',
        labels={'x': 'Product Name', 'y': 'Total Revenue ($)'}
    )
    bar_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    bar_plot_html = bar_fig.to_html(full_html=False)

    # Plot 3: Pie chart for revenue distribution by category
    pie_fig = px.pie(
        df,
        names='Category',
        values='Monthly Revenue',
        title='Revenue Distribution by Category'
    )
    pie_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    pie_plot_html = pie_fig.to_html(full_html=False)

    # Plot 4: Scatter plot for revenue vs. number of units sold
    scatter_fig = px.scatter(
        df,
        x='Monthly Revenue',
        y='Monthly Sales Volume (units)',
        title='Revenue vs. Number of Units Sold',
        labels={'x': 'Revenue ($)', 'y': 'Units Sold'}
    )
    scatter_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    scatter_plot_html = scatter_fig.to_html(full_html=False)

    # Plot 5: Box plot for revenue distribution across product categories
    box_fig = px.box(
        df,
        x='Category',
        y='Monthly Revenue',
        title='Revenue Distribution Across Categories',
        labels={'x': 'Category', 'y': 'Revenue ($)'}
    )
    box_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    box_plot_html = box_fig.to_html(full_html=False)

    # Plot 6: Histogram for the distribution of monthly revenues
    hist_fig = px.histogram(
        df,
        x='Monthly Revenue',
        title='Distribution of Monthly Revenues',
        labels={'x': 'Revenue ($)'}
    )
    hist_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    hist_plot_html = hist_fig.to_html(full_html=False)

    # Plot 7: Heatmap for the correlation matrix
    numeric_cols = df.select_dtypes(include='number')  # Select only numeric columns
    corr_matrix = numeric_cols.corr()
    heatmap_fig = px.imshow(
        corr_matrix,
        title='Correlation Matrix of Revenue Features',
        labels=dict(color='Correlation')
    )
    heatmap_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    heatmap_plot_html = heatmap_fig.to_html(full_html=False)

    # Plot 8: Violin plot for revenue distribution by customer type (if it exists)
    if 'Customer type' in df.columns:
        violin_fig = px.violin(
            df,
            x='Customer type',
            y='Monthly Revenue',
            title='Revenue Distribution by Customer Type',
            labels={'x': 'Customer Type', 'y': 'Revenue ($)'},
            box=True,
            points='all'
        )
        violin_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
        violin_plot_html = violin_fig.to_html(full_html=False)
    else:
        violin_plot_html = None

    # Plot 9: Sunburst plot for revenue breakdown by city and category (if 'City' exists)
    if 'City' in df.columns:
        sunburst_fig = px.sunburst(
            df,
            path=['City', 'Category'],
            values='Monthly Revenue',
            title='Revenue Breakdown by City and Category'
        )
        sunburst_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
        sunburst_plot_html = sunburst_fig.to_html(full_html=False)
    else:
        sunburst_plot_html = None

    # Plot 10: Area plot for cumulative revenue over time
    area_fig = px.area(
        df.sort_values(by='Sales Month'),
        x='Sales Month',
        y='Monthly Revenue',
        title='Cumulative Revenue Over Time',
        labels={'x': 'Month', 'y': 'Cumulative Revenue ($)'}
    )
    area_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), autosize=False, height=350, width=500, title_x=0.5)
    area_plot_html = area_fig.to_html(full_html=False)

    # Pass the plots to the template
    context = {
        'line_plot': line_plot_html,
        'bar_plot': bar_plot_html,
        'pie_plot': pie_plot_html,
        'scatter_plot': scatter_plot_html,
        'box_plot': box_plot_html,
        'hist_plot': hist_plot_html,
        'heatmap_plot': heatmap_plot_html,
        'violin_plot': violin_plot_html,
        'sunburst_plot': sunburst_plot_html,
        'area_plot': area_plot_html,
    }
    return render(request, 'dashboard_app/total_revenue_detail.html', context)








##################################

# Load your dataset (ensure this path points to your dataset)

# Load your dataset (ensure this path points to your dataset)
df = pd.read_csv('Datasets/Ispahani.csv')

# Convert relevant columns to numeric, handling non-numeric values
numeric_columns = ['Monthly Sales Volume (units)', 'Monthly Revenue', 'Price/Unit', 'Total Weight/Carton']
for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Drop rows with NaN values in numeric columns to avoid plotting issues
df = df.dropna(subset=numeric_columns)

def top_selling_product(request):
    try:
        # 1. Treemap for Revenue by Category and Product
        treemap_fig = px.treemap(
            df,
            path=['Category', 'Product Name'],
            values='Monthly Revenue',
            title='Revenue Breakdown by Category and Product'
        )
        treemap_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_plot_html = treemap_fig.to_html(full_html=False)

        # 2. Funnel Plot for Sales Volume Across Product Categories
        funnel_fig = px.funnel(
            df,
            x='Category',
            y='Monthly Sales Volume (units)',
            title='Sales Volume Funnel by Product Category'
        )
        funnel_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        funnel_plot_html = funnel_fig.to_html(full_html=False)

        # 3. Box Plot for Product Prices by Category
        box_price_fig = px.box(
            df,
            x='Category',
            y='Price/Unit',
            title='Distribution of Product Prices by Category'
        )
        box_price_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_price_plot_html = box_price_fig.to_html(full_html=False)

        # 4. Scatter Matrix for Relationship Analysis
        scatter_matrix_fig = px.scatter_matrix(
            df,
            dimensions=['Monthly Sales Volume (units)', 'Monthly Revenue', 'Price/Unit'],
            color='Category',
            title='Scatter Matrix of Sales and Revenue Features'
        )
        scatter_matrix_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=500, width=800, title_x=0.5)
        scatter_matrix_plot_html = scatter_matrix_fig.to_html(full_html=False)

        # 5. Density Heatmap for Monthly Revenue and Units Sold
        density_fig = px.density_heatmap(
            df,
            x='Monthly Revenue',
            y='Monthly Sales Volume (units)',
            title='Density Heatmap of Revenue vs. Units Sold'
        )
        density_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_plot_html = density_fig.to_html(full_html=False)

        # 6. Parallel Coordinates Plot for Sales Features
        parallel_fig = px.parallel_coordinates(
            df,
            dimensions=['Monthly Sales Volume (units)', 'Monthly Revenue', 'Price/Unit'],
            color='Monthly Revenue',
            title='Parallel Coordinates Plot of Sales Features'
        )
        parallel_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=800, title_x=0.5)
        parallel_plot_html = parallel_fig.to_html(full_html=False)

        # 7. Bar Plot for Top 10 Products by Revenue
        top_revenue_products = df.groupby('Product Name')['Monthly Revenue'].sum().sort_values(ascending=False).head(10)
        revenue_bar_fig = px.bar(
            x=top_revenue_products.index,
            y=top_revenue_products.values,
            title='Top 10 Products by Revenue',
            labels={'x': 'Product Name', 'y': 'Revenue ($)'}
        )
        revenue_bar_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        revenue_bar_plot_html = revenue_bar_fig.to_html(full_html=False)

        # 8. Histogram for Product Shelf Life
        hist_shelf_life_fig = px.histogram(
            df,
            x='Shelf Life',
            title='Distribution of Product Shelf Life',
            labels={'Shelf Life': 'Shelf Life (Days)'}
        )
        hist_shelf_life_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_shelf_life_plot_html = hist_shelf_life_fig.to_html(full_html=False)

        # 9. Line Plot for Revenue Trends by Category Over Time
        line_category_fig = px.line(
            df,
            x='Sales Month',
            y='Monthly Revenue',
            color='Category',
            title='Revenue Trends by Category Over Time',
            labels={'Sales Month': 'Month', 'Monthly Revenue': 'Revenue ($)'}
        )
        line_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_category_plot_html = line_category_fig.to_html(full_html=False)

        # 10. Pie Chart for Revenue Distribution by Category
        pie_category_fig = px.pie(
            df,
            names='Category',
            values='Monthly Revenue',
            title='Revenue Distribution by Category'
        )
        pie_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_category_plot_html = pie_category_fig.to_html(full_html=False)

        context = {
            'treemap_plot': treemap_plot_html,
            'funnel_plot': funnel_plot_html,
            'box_price_plot': box_price_plot_html,
            'scatter_matrix_plot': scatter_matrix_plot_html,
            'density_plot': density_plot_html,
            'parallel_plot': parallel_plot_html,
            'revenue_bar_plot': revenue_bar_plot_html,
            'hist_shelf_life_plot': hist_shelf_life_plot_html,
            'line_category_plot': line_category_plot_html,
            'pie_category_plot': pie_category_plot_html,
        }

        return render(request, 'dashboard_app/top_selling_product.html', context)

    except Exception as e:
        # Handle and display any unexpected errors gracefully
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})





##################################


def category_analysis_detail(request):
    try:
        # 1. Bar Plot for Total Revenue by Category
        revenue_category_fig = px.bar(
            df.groupby('Category')['Monthly Revenue'].sum().sort_values(ascending=False),
            title='Total Revenue by Category',
            labels={'index': 'Category', 'value': 'Total Revenue ($)'}
        )
        revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        revenue_category_plot_html = revenue_category_fig.to_html(full_html=False)

        # 2. Pie Chart for Sales Distribution by Category
        pie_sales_category_fig = px.pie(
            df,
            names='Category',
            values='Monthly Sales Volume (units)',
            title='Sales Distribution by Category'
        )
        pie_sales_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_sales_category_plot_html = pie_sales_category_fig.to_html(full_html=False)

        # 3. Line Plot for Monthly Revenue Trends by Category
        line_revenue_category_fig = px.line(
            df,
            x='Sales Month',
            y='Monthly Revenue',
            color='Category',
            title='Monthly Revenue Trends by Category',
            labels={'Sales Month': 'Month', 'Monthly Revenue': 'Revenue ($)'}
        )
        line_revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_revenue_category_plot_html = line_revenue_category_fig.to_html(full_html=False)

        # 4. Box Plot for Monthly Revenue by Category
        box_revenue_category_fig = px.box(
            df,
            x='Category',
            y='Monthly Revenue',
            title='Distribution of Monthly Revenue by Category'
        )
        box_revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_revenue_category_plot_html = box_revenue_category_fig.to_html(full_html=False)

        # 5. Violin Plot for Monthly Sales Volume by Category
        violin_sales_category_fig = px.violin(
            df,
            x='Category',
            y='Monthly Sales Volume (units)',
            box=True,
            title='Distribution of Monthly Sales Volume by Category'
        )
        violin_sales_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_sales_category_plot_html = violin_sales_category_fig.to_html(full_html=False)

        # 6. Sunburst Plot for Revenue by Category and Product
        sunburst_revenue_fig = px.sunburst(
            df,
            path=['Category', 'Product Name'],
            values='Monthly Revenue',
            title='Revenue Distribution by Category and Product'
        )
        sunburst_revenue_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        sunburst_revenue_plot_html = sunburst_revenue_fig.to_html(full_html=False)

        # 7. Treemap for Sales Volume by Category and Product
        treemap_sales_fig = px.treemap(
            df,
            path=['Category', 'Product Name'],
            values='Monthly Sales Volume (units)',
            title='Sales Volume by Category and Product'
        )
        treemap_sales_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_sales_plot_html = treemap_sales_fig.to_html(full_html=False)

        # 8. Histogram for Revenue Distribution Across Categories
        hist_revenue_category_fig = px.histogram(
            df,
            x='Category',
            y='Monthly Revenue',
            title='Revenue Distribution Across Categories',
            labels={'Monthly Revenue': 'Revenue ($)'}
        )
        hist_revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_revenue_category_plot_html = hist_revenue_category_fig.to_html(full_html=False)

        # 9. Scatter Plot for Price vs Revenue by Category
        scatter_price_revenue_fig = px.scatter(
            df,
            x='Price/Unit',
            y='Monthly Revenue',
            color='Category',
            title='Price vs Revenue by Category',
            labels={'Price/Unit': 'Price per Unit', 'Monthly Revenue': 'Revenue ($)'}
        )
        scatter_price_revenue_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_price_revenue_plot_html = scatter_price_revenue_fig.to_html(full_html=False)

        # 10. Parallel Categories Plot for Category and Product Analysis
        parallel_categories_fig = px.parallel_categories(
            df,
            dimensions=['Category', 'Product Name'],
            title='Parallel Categories for Category and Product Analysis'
        )
        parallel_categories_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        parallel_categories_plot_html = parallel_categories_fig.to_html(full_html=False)

        context = {
            'revenue_category_plot': revenue_category_plot_html,
            'pie_sales_category_plot': pie_sales_category_plot_html,
            'line_revenue_category_plot': line_revenue_category_plot_html,
            'box_revenue_category_plot': box_revenue_category_plot_html,
            'violin_sales_category_plot': violin_sales_category_plot_html,
            'sunburst_revenue_plot': sunburst_revenue_plot_html,
            'treemap_sales_plot': treemap_sales_plot_html,
            'hist_revenue_category_plot': hist_revenue_category_plot_html,
            'scatter_price_revenue_plot': scatter_price_revenue_plot_html,
            'parallel_categories_plot': parallel_categories_plot_html,
        }

        return render(request, 'dashboard_app/category_analysis_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})



################################################################

def monthly_sales_detail(request):
    try:
        # 1. Area Plot for Monthly Sales Volume Over Time
        area_sales_volume_fig = px.area(
            df,
            x='Sales Month',
            y='Monthly Sales Volume (units)',
            title='Monthly Sales Volume Over Time',
            labels={'Sales Month': 'Month', 'Monthly Sales Volume (units)': 'Units Sold'}
        )
        area_sales_volume_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_sales_volume_plot_html = area_sales_volume_fig.to_html(full_html=False)

        # 2. Treemap for Average Monthly Sales by Category
        treemap_sales_category_fig = px.treemap(
            df,
            path=['Category'],
            values='Monthly Sales Volume (units)',
            title='Treemap of Monthly Sales by Category'
        )
        treemap_sales_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_sales_category_plot_html = treemap_sales_category_fig.to_html(full_html=False)

        # 3. Funnel Plot for Monthly Sales by Product
        funnel_sales_volume_fig = px.funnel(
            df,
            x='Product Name',
            y='Monthly Sales Volume (units)',
            title='Monthly Sales Funnel by Product'
        )
        funnel_sales_volume_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        funnel_sales_volume_plot_html = funnel_sales_volume_fig.to_html(full_html=False)

        # 4. Sunburst Plot for Monthly Sales by Category and Product
        sunburst_sales_volume_fig = px.sunburst(
            df,
            path=['Category', 'Product Name'],
            values='Monthly Sales Volume (units)',
            title='Sunburst of Monthly Sales by Category and Product'
        )
        sunburst_sales_volume_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        sunburst_sales_volume_plot_html = sunburst_sales_volume_fig.to_html(full_html=False)

        # 5. Box Plot for Monthly Revenue by Category
        box_revenue_category_fig = px.box(
            df,
            x='Category',
            y='Monthly Revenue',
            title='Monthly Revenue by Category'
        )
        box_revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_revenue_category_plot_html = box_revenue_category_fig.to_html(full_html=False)

        # 6. Density Contour Plot for Price vs Revenue
        density_contour_fig = px.density_contour(
            df,
            x='Price/Unit',
            y='Monthly Revenue',
            title='Price vs Revenue Density Contour',
            labels={'Price/Unit': 'Price per Unit', 'Monthly Revenue': 'Revenue ($)'}
        )
        density_contour_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_contour_plot_html = density_contour_fig.to_html(full_html=False)

        # 7. Violin Plot for Monthly Sales Volume by Product
        violin_sales_product_fig = px.violin(
            df,
            x='Product Name',
            y='Monthly Sales Volume (units)',
            box=True,
            title='Violin Plot of Monthly Sales by Product'
        )
        violin_sales_product_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_sales_product_plot_html = violin_sales_product_fig.to_html(full_html=False)

        # 8. Scatter Plot for Revenue vs. Monthly Sales Volume with Category Highlight
        scatter_revenue_sales_fig = px.scatter(
            df,
            x='Monthly Sales Volume (units)',
            y='Monthly Revenue',
            color='Category',
            title='Revenue vs. Monthly Sales Volume by Category',
            labels={'Monthly Sales Volume (units)': 'Units Sold', 'Monthly Revenue': 'Revenue ($)'}
        )
        scatter_revenue_sales_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_revenue_sales_plot_html = scatter_revenue_sales_fig.to_html(full_html=False)

        # 9. Pie Chart for Monthly Revenue by Category
        pie_revenue_category_fig = px.pie(
            df,
            names='Category',
            values='Monthly Revenue',
            title='Monthly Revenue by Category'
        )
        pie_revenue_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_revenue_category_plot_html = pie_revenue_category_fig.to_html(full_html=False)

        # 10. Line Plot for Price Changes Over Time by Product
        line_price_change_fig = px.line(
            df,
            x='Sales Month',
            y='Price/Unit',
            color='Product Name',
            title='Price Changes Over Time by Product',
            labels={'Sales Month': 'Month', 'Price/Unit': 'Price per Unit'}
        )
        line_price_change_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_price_change_plot_html = line_price_change_fig.to_html(full_html=False)

        context = {
            'area_sales_volume_plot': area_sales_volume_plot_html,
            'treemap_sales_category_plot': treemap_sales_category_plot_html,
            'funnel_sales_volume_plot': funnel_sales_volume_plot_html,
            'sunburst_sales_volume_plot': sunburst_sales_volume_plot_html,
            'box_revenue_category_plot': box_revenue_category_plot_html,
            'density_contour_plot': density_contour_plot_html,
            'violin_sales_product_plot': violin_sales_product_plot_html,
            'scatter_revenue_sales_plot': scatter_revenue_sales_plot_html,
            'pie_revenue_category_plot': pie_revenue_category_plot_html,
            'line_price_change_plot': line_price_change_plot_html,
        }

        return render(request, 'dashboard_app/monthly_sales_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})











################################################################


def profit_margin_detail(request):
    try:
        # Calculate Profit Margin as a new column
        df['Profit Margin'] = (df['Monthly Revenue'] - df['Price/Unit'] * df['Monthly Sales Volume (units)']) / df['Monthly Revenue'] * 100

        # 1. Line Plot for Profit Margin Over Time
        line_profit_margin_fig = px.line(
            df,
            x='Sales Month',
            y='Profit Margin',
            title='Profit Margin Over Time',
            labels={'Sales Month': 'Month', 'Profit Margin': 'Profit Margin (%)'}
        )
        line_profit_margin_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_profit_margin_plot_html = line_profit_margin_fig.to_html(full_html=False)

        # 2. Bar Plot for Average Profit Margin by Category
        avg_profit_category = df.groupby('Category')['Profit Margin'].mean().sort_values(ascending=False)
        bar_avg_profit_category_fig = px.bar(
            x=avg_profit_category.index,
            y=avg_profit_category.values,
            title='Average Profit Margin by Category',
            labels={'x': 'Category', 'y': 'Average Profit Margin (%)'}
        )
        bar_avg_profit_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        bar_avg_profit_category_plot_html = bar_avg_profit_category_fig.to_html(full_html=False)

        # 3. Scatter Plot for Revenue vs. Profit Margin by Category
        scatter_revenue_profit_fig = px.scatter(
            df,
            x='Monthly Revenue',
            y='Profit Margin',
            color='Category',
            title='Revenue vs. Profit Margin by Category',
            labels={'Monthly Revenue': 'Revenue ($)', 'Profit Margin': 'Profit Margin (%)'}
        )
        scatter_revenue_profit_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_revenue_profit_plot_html = scatter_revenue_profit_fig.to_html(full_html=False)

        # 4. Violin Plot for Profit Margin by Product
        violin_profit_product_fig = px.violin(
            df,
            x='Product Name',
            y='Profit Margin',
            box=True,
            title='Profit Margin by Product'
        )
        violin_profit_product_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_profit_product_plot_html = violin_profit_product_fig.to_html(full_html=False)

        # 5. Density Heatmap for Profit Margin and Monthly Revenue
        density_heatmap_profit_fig = px.density_heatmap(
            df,
            x='Monthly Revenue',
            y='Profit Margin',
            title='Density Heatmap of Profit Margin and Monthly Revenue',
            labels={'Monthly Revenue': 'Revenue ($)', 'Profit Margin': 'Profit Margin (%)'}
        )
        density_heatmap_profit_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_heatmap_profit_plot_html = density_heatmap_profit_fig.to_html(full_html=False)

        # 6. Pie Chart for Share of Total Profit Margin by Category
        pie_profit_category_fig = px.pie(
            df,
            names='Category',
            values='Profit Margin',
            title='Share of Total Profit Margin by Category'
        )
        pie_profit_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_profit_category_plot_html = pie_profit_category_fig.to_html(full_html=False)

        # 7. Box Plot for Profit Margin Distribution by Category
        box_profit_category_fig = px.box(
            df,
            x='Category',
            y='Profit Margin',
            title='Profit Margin Distribution by Category'
        )
        box_profit_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_profit_category_plot_html = box_profit_category_fig.to_html(full_html=False)

        # 8. Area Plot for Cumulative Profit Margin Over Time
        df['Cumulative Profit Margin'] = df['Profit Margin'].cumsum()
        area_cumulative_profit_fig = px.area(
            df,
            x='Sales Month',
            y='Cumulative Profit Margin',
            title='Cumulative Profit Margin Over Time',
            labels={'Sales Month': 'Month', 'Cumulative Profit Margin': 'Cumulative Profit Margin (%)'}
        )
        area_cumulative_profit_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_cumulative_profit_plot_html = area_cumulative_profit_fig.to_html(full_html=False)

        # 9. Treemap for Profit Margin by Category and Product
        treemap_profit_fig = px.treemap(
            df,
            path=['Category', 'Product Name'],
            values='Profit Margin',
            title='Profit Margin by Category and Product'
        )
        treemap_profit_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_profit_plot_html = treemap_profit_fig.to_html(full_html=False)

        # 10. Histogram for Profit Margin Distribution
        hist_profit_margin_fig = px.histogram(
            df,
            x='Profit Margin',
            title='Distribution of Profit Margin',
            labels={'Profit Margin': 'Profit Margin (%)'}
        )
        hist_profit_margin_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_profit_margin_plot_html = hist_profit_margin_fig.to_html(full_html=False)

        context = {
            'line_profit_margin_plot': line_profit_margin_plot_html,
            'bar_avg_profit_category_plot': bar_avg_profit_category_plot_html,
            'scatter_revenue_profit_plot': scatter_revenue_profit_plot_html,
            'violin_profit_product_plot': violin_profit_product_plot_html,
            'density_heatmap_profit_plot': density_heatmap_profit_plot_html,
            'pie_profit_category_plot': pie_profit_category_plot_html,
            'box_profit_category_plot': box_profit_category_plot_html,
            'area_cumulative_profit_plot': area_cumulative_profit_plot_html,
            'treemap_profit_plot': treemap_profit_plot_html,
            'hist_profit_margin_plot': hist_profit_margin_plot_html,
        }

        return render(request, 'dashboard_app/profit_margin_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})













################################################################

def shelf_life_detail(request):
    try:
        # 1. Histogram for Distribution of Shelf Life
        hist_shelf_life_fig = px.histogram(
            df,
            x='Shelf Life',
            title='Distribution of Shelf Life',
            labels={'Shelf Life': 'Shelf Life (days)'}
        )
        hist_shelf_life_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_shelf_life_plot_html = hist_shelf_life_fig.to_html(full_html=False)

        # 2. Box Plot for Shelf Life by Category
        box_shelf_life_category_fig = px.box(
            df,
            x='Category',
            y='Shelf Life',
            title='Shelf Life by Category'
        )
        box_shelf_life_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_shelf_life_category_plot_html = box_shelf_life_category_fig.to_html(full_html=False)

        # 3. Bar Plot for Average Shelf Life by Category
        avg_shelf_life_category = df.groupby('Category')['Shelf Life'].mean().sort_values(ascending=False)
        bar_avg_shelf_life_category_fig = px.bar(
            x=avg_shelf_life_category.index,
            y=avg_shelf_life_category.values,
            title='Average Shelf Life by Category',
            labels={'x': 'Category', 'y': 'Average Shelf Life (days)'}
        )
        bar_avg_shelf_life_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        bar_avg_shelf_life_category_plot_html = bar_avg_shelf_life_category_fig.to_html(full_html=False)

        # 4. Violin Plot for Shelf Life Distribution by Product
        violin_shelf_life_product_fig = px.violin(
            df,
            x='Product Name',
            y='Shelf Life',
            box=True,
            title='Shelf Life Distribution by Product'
        )
        violin_shelf_life_product_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_shelf_life_product_plot_html = violin_shelf_life_product_fig.to_html(full_html=False)

        # 5. Scatter Plot for Shelf Life vs. Price per Unit
        scatter_shelf_price_fig = px.scatter(
            df,
            x='Price/Unit',
            y='Shelf Life',
            title='Shelf Life vs. Price per Unit',
            labels={'Price/Unit': 'Price per Unit', 'Shelf Life': 'Shelf Life (days)'},
            color='Category'
        )
        scatter_shelf_price_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_shelf_price_plot_html = scatter_shelf_price_fig.to_html(full_html=False)

        # 6. Pie Chart for Proportion of Products by Shelf Life Range
        df['Shelf Life Range'] = pd.cut(df['Shelf Life'], bins=[0, 30, 90, 180, 365, 730], labels=['0-30', '31-90', '91-180', '181-365', '366-730'])
        pie_shelf_life_range_fig = px.pie(
            df,
            names='Shelf Life Range',
            title='Proportion of Products by Shelf Life Range'
        )
        pie_shelf_life_range_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_shelf_life_range_plot_html = pie_shelf_life_range_fig.to_html(full_html=False)

        # 7. Line Plot for Shelf Life Trends Over Time
        line_shelf_life_trend_fig = px.line(
            df,
            x='Sales Month',
            y='Shelf Life',
            title='Shelf Life Trends Over Time',
            labels={'Sales Month': 'Month', 'Shelf Life': 'Shelf Life (days)'}
        )
        line_shelf_life_trend_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_shelf_life_trend_plot_html = line_shelf_life_trend_fig.to_html(full_html=False)

        # 8. Treemap for Shelf Life by Category and Product
        treemap_shelf_life_fig = px.treemap(
            df,
            path=['Category', 'Product Name'],
            values='Shelf Life',
            title='Shelf Life by Category and Product'
        )
        treemap_shelf_life_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_shelf_life_plot_html = treemap_shelf_life_fig.to_html(full_html=False)

        # 9. Area Plot for Cumulative Shelf Life Distribution
        df['Cumulative Shelf Life'] = df['Shelf Life'].cumsum()
        area_cumulative_shelf_life_fig = px.area(
            df,
            x='Sales Month',
            y='Cumulative Shelf Life',
            title='Cumulative Shelf Life Distribution',
            labels={'Sales Month': 'Month', 'Cumulative Shelf Life': 'Cumulative Shelf Life (days)'}
        )
        area_cumulative_shelf_life_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_cumulative_shelf_life_plot_html = area_cumulative_shelf_life_fig.to_html(full_html=False)

        # 10. Histogram for Shelf Life Distribution by Price Range
        hist_shelf_price_range_fig = px.histogram(
            df,
            x='Price/Unit',
            y='Shelf Life',
            title='Shelf Life Distribution by Price Range',
            labels={'Price/Unit': 'Price per Unit', 'Shelf Life': 'Shelf Life (days)'}
        )
        hist_shelf_price_range_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_shelf_price_range_plot_html = hist_shelf_price_range_fig.to_html(full_html=False)

        context = {
            'hist_shelf_life_plot': hist_shelf_life_plot_html,
            'box_shelf_life_category_plot': box_shelf_life_category_plot_html,
            'bar_avg_shelf_life_category_plot': bar_avg_shelf_life_category_plot_html,
            'violin_shelf_life_product_plot': violin_shelf_life_product_plot_html,
            'scatter_shelf_price_plot': scatter_shelf_price_plot_html,
            'pie_shelf_life_range_plot': pie_shelf_life_range_plot_html,
            'line_shelf_life_trend_plot': line_shelf_life_trend_plot_html,
            'treemap_shelf_life_plot': treemap_shelf_life_plot_html,
            'area_cumulative_shelf_life_plot': area_cumulative_shelf_life_plot_html,
            'hist_shelf_price_range_plot': hist_shelf_price_range_plot_html,
        }

        return render(request, 'dashboard_app/shelf_life_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})








################################################################
def sales_growth_detail(request):
    try:
        # 1. Line Plot for Monthly Growth Rate Over Time
        line_growth_rate_fig = px.line(
            df,
            x='Sales Month',
            y='Monthly Growth Rate',
            title='Monthly Growth Rate Over Time',
            labels={'Sales Month': 'Month', 'Monthly Growth Rate': 'Growth Rate (%)'}
        )
        line_growth_rate_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_growth_rate_plot_html = line_growth_rate_fig.to_html(full_html=False)

        # 2. Bar Plot for Average Growth Rate by Category
        avg_growth_category = df.groupby('Category')['Monthly Growth Rate'].mean().sort_values(ascending=False)
        bar_avg_growth_category_fig = px.bar(
            x=avg_growth_category.index,
            y=avg_growth_category.values,
            title='Average Growth Rate by Category',
            labels={'x': 'Category', 'y': 'Average Growth Rate (%)'}
        )
        bar_avg_growth_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        bar_avg_growth_category_plot_html = bar_avg_growth_category_fig.to_html(full_html=False)

        # 3. Scatter Plot for Sales Growth vs. Revenue
        scatter_growth_revenue_fig = px.scatter(
            df,
            x='Monthly Revenue',
            y='Monthly Growth Rate',
            color='Category',
            title='Sales Growth vs. Revenue by Category',
            labels={'Monthly Revenue': 'Revenue ($)', 'Monthly Growth Rate': 'Growth Rate (%)'}
        )
        scatter_growth_revenue_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_growth_revenue_plot_html = scatter_growth_revenue_fig.to_html(full_html=False)

        # 4. Box Plot for Growth Rate by Category
        box_growth_category_fig = px.box(
            df,
            x='Category',
            y='Monthly Growth Rate',
            title='Growth Rate Distribution by Category'
        )
        box_growth_category_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_growth_category_plot_html = box_growth_category_fig.to_html(full_html=False)

        # 5. Pie Chart for Growth Rate Share by Product
        pie_growth_product_fig = px.pie(
            df,
            names='Product Name',
            values='Monthly Growth Rate',
            title='Share of Growth Rate by Product'
        )
        pie_growth_product_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_growth_product_plot_html = pie_growth_product_fig.to_html(full_html=False)

        # 6. Treemap for Growth Rate by Category and Product
        treemap_growth_fig = px.treemap(
            df,
            path=['Category', 'Product Name'],
            values='Monthly Growth Rate',
            title='Growth Rate by Category and Product'
        )
        treemap_growth_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_growth_plot_html = treemap_growth_fig.to_html(full_html=False)

        # 7. Histogram for Distribution of Growth Rate
        hist_growth_rate_fig = px.histogram(
            df,
            x='Monthly Growth Rate',
            title='Distribution of Growth Rate',
            labels={'Monthly Growth Rate': 'Growth Rate (%)'}
        )
        hist_growth_rate_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_growth_rate_plot_html = hist_growth_rate_fig.to_html(full_html=False)

        # 8. Violin Plot for Growth Rate by Product
        violin_growth_product_fig = px.violin(
            df,
            x='Product Name',
            y='Monthly Growth Rate',
            box=True,
            title='Growth Rate by Product'
        )
        violin_growth_product_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_growth_product_plot_html = violin_growth_product_fig.to_html(full_html=False)

        # 9. Density Heatmap for Growth Rate and Revenue
        density_heatmap_growth_fig = px.density_heatmap(
            df,
            x='Monthly Revenue',
            y='Monthly Growth Rate',
            title='Density Heatmap of Growth Rate and Revenue',
            labels={'Monthly Revenue': 'Revenue ($)', 'Monthly Growth Rate': 'Growth Rate (%)'}
        )
        density_heatmap_growth_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_heatmap_growth_plot_html = density_heatmap_growth_fig.to_html(full_html=False)

        # 10. Area Plot for Cumulative Growth Rate Over Time
        df['Cumulative Growth Rate'] = df['Monthly Growth Rate'].cumsum()
        area_cumulative_growth_fig = px.area(
            df,
            x='Sales Month',
            y='Cumulative Growth Rate',
            title='Cumulative Growth Rate Over Time',
            labels={'Sales Month': 'Month', 'Cumulative Growth Rate': 'Cumulative Growth Rate (%)'}
        )
        area_cumulative_growth_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_cumulative_growth_plot_html = area_cumulative_growth_fig.to_html(full_html=False)

        context = {
            'line_growth_rate_plot': line_growth_rate_plot_html,
            'bar_avg_growth_category_plot': bar_avg_growth_category_plot_html,
            'scatter_growth_revenue_plot': scatter_growth_revenue_plot_html,
            'box_growth_category_plot': box_growth_category_plot_html,
            'pie_growth_product_plot': pie_growth_product_plot_html,
            'treemap_growth_plot': treemap_growth_plot_html,
            'hist_growth_rate_plot': hist_growth_rate_plot_html,
            'violin_growth_product_plot': violin_growth_product_plot_html,
            'density_heatmap_growth_plot': density_heatmap_growth_plot_html,
            'area_cumulative_growth_plot': area_cumulative_growth_plot_html,
        }

        return render(request, 'dashboard_app/sales_growth_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})










################################################################
def revenue_flavor_detail(request):
    try:
        # 1. Bar Plot for Total Revenue by Flavor
        bar_revenue_flavor_fig = px.bar(
            df,
            x='Flavor',
            y='Monthly Revenue',
            title='Total Revenue by Flavor',
            labels={'Flavor': 'Flavor', 'Monthly Revenue': 'Revenue ($)'},
            color='Flavor'
        )
        bar_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        bar_revenue_flavor_plot_html = bar_revenue_flavor_fig.to_html(full_html=False)

        # 2. Pie Chart for Revenue Share by Flavor
        pie_revenue_flavor_fig = px.pie(
            df,
            names='Flavor',
            values='Monthly Revenue',
            title='Revenue Share by Flavor'
        )
        pie_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_revenue_flavor_plot_html = pie_revenue_flavor_fig.to_html(full_html=False)

        # 3. Scatter Plot for Revenue vs. Price per Unit by Flavor
        scatter_revenue_price_fig = px.scatter(
            df,
            x='Price/Unit',
            y='Monthly Revenue',
            color='Flavor',
            title='Revenue vs. Price per Unit by Flavor',
            labels={'Price/Unit': 'Price per Unit', 'Monthly Revenue': 'Revenue ($)'}
        )
        scatter_revenue_price_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_revenue_price_plot_html = scatter_revenue_price_fig.to_html(full_html=False)

        # 4. Box Plot for Revenue Distribution by Flavor
        box_revenue_flavor_fig = px.box(
            df,
            x='Flavor',
            y='Monthly Revenue',
            title='Revenue Distribution by Flavor'
        )
        box_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_revenue_flavor_plot_html = box_revenue_flavor_fig.to_html(full_html=False)

        # 5. Histogram for Revenue Distribution by Flavor
        hist_revenue_flavor_fig = px.histogram(
            df,
            x='Flavor',
            y='Monthly Revenue',
            title='Revenue Distribution by Flavor',
            labels={'Flavor': 'Flavor', 'Monthly Revenue': 'Revenue ($)'},
            color='Flavor'
        )
        hist_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_revenue_flavor_plot_html = hist_revenue_flavor_fig.to_html(full_html=False)

        # 6. Violin Plot for Revenue by Flavor
        violin_revenue_flavor_fig = px.violin(
            df,
            x='Flavor',
            y='Monthly Revenue',
            box=True,
            title='Revenue by Flavor'
        )
        violin_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_revenue_flavor_plot_html = violin_revenue_flavor_fig.to_html(full_html=False)

        # 7. Treemap for Revenue by Flavor and Product
        treemap_revenue_flavor_fig = px.treemap(
            df,
            path=['Flavor', 'Product Name'],
            values='Monthly Revenue',
            title='Revenue by Flavor and Product'
        )
        treemap_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_revenue_flavor_plot_html = treemap_revenue_flavor_fig.to_html(full_html=False)

        # 8. Line Plot for Revenue Trends Over Time by Flavor
        line_revenue_trend_flavor_fig = px.line(
            df,
            x='Sales Month',
            y='Monthly Revenue',
            color='Flavor',
            title='Revenue Trends Over Time by Flavor',
            labels={'Sales Month': 'Month', 'Monthly Revenue': 'Revenue ($)'}
        )
        line_revenue_trend_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_revenue_trend_flavor_plot_html = line_revenue_trend_flavor_fig.to_html(full_html=False)

        # 9. Area Plot for Cumulative Revenue by Flavor
        df['Cumulative Revenue'] = df.groupby('Flavor')['Monthly Revenue'].cumsum()
        area_cumulative_revenue_flavor_fig = px.area(
            df,
            x='Sales Month',
            y='Cumulative Revenue',
            color='Flavor',
            title='Cumulative Revenue by Flavor',
            labels={'Sales Month': 'Month', 'Cumulative Revenue': 'Cumulative Revenue ($)'}
        )
        area_cumulative_revenue_flavor_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_cumulative_revenue_flavor_plot_html = area_cumulative_revenue_flavor_fig.to_html(full_html=False)

        # 10. Density Heatmap for Revenue and Sales Volume by Flavor
        density_heatmap_revenue_volume_fig = px.density_heatmap(
            df,
            x='Monthly Sales Volume (units)',
            y='Monthly Revenue',
            z='Flavor',
            title='Density Heatmap of Revenue and Sales Volume by Flavor',
            labels={'Monthly Sales Volume (units)': 'Sales Volume (units)', 'Monthly Revenue': 'Revenue ($)'}
        )
        density_heatmap_revenue_volume_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_heatmap_revenue_volume_plot_html = density_heatmap_revenue_volume_fig.to_html(full_html=False)

        context = {
            'bar_revenue_flavor_plot': bar_revenue_flavor_plot_html,
            'pie_revenue_flavor_plot': pie_revenue_flavor_plot_html,
            'scatter_revenue_price_plot': scatter_revenue_price_plot_html,
            'box_revenue_flavor_plot': box_revenue_flavor_plot_html,
            'hist_revenue_flavor_plot': hist_revenue_flavor_plot_html,
            'violin_revenue_flavor_plot': violin_revenue_flavor_plot_html,
            'treemap_revenue_flavor_plot': treemap_revenue_flavor_plot_html,
            'line_revenue_trend_flavor_plot': line_revenue_trend_flavor_plot_html,
            'area_cumulative_revenue_flavor_plot': area_cumulative_revenue_flavor_plot_html,
            'density_heatmap_revenue_volume_plot': density_heatmap_revenue_volume_plot_html,
        }

        return render(request, 'dashboard_app/revenue_flavor_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})







################################################################
def revenue_packaging_detail(request):
    try:
        # 1. Bar Plot for Total Revenue by Packaging Type
        bar_revenue_packaging_fig = px.bar(
            df,
            x='Pack Type',
            y='Monthly Revenue',
            title='Total Revenue by Packaging Type',
            labels={'Pack Type': 'Packaging Type', 'Monthly Revenue': 'Revenue ($)'},
            color='Pack Type'
        )
        bar_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        bar_revenue_packaging_plot_html = bar_revenue_packaging_fig.to_html(full_html=False)

        # 2. Pie Chart for Revenue Share by Packaging Type
        pie_revenue_packaging_fig = px.pie(
            df,
            names='Pack Type',
            values='Monthly Revenue',
            title='Revenue Share by Packaging Type'
        )
        pie_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        pie_revenue_packaging_plot_html = pie_revenue_packaging_fig.to_html(full_html=False)

        # 3. Scatter Plot for Revenue vs. Price per Unit by Packaging Type
        scatter_revenue_price_packaging_fig = px.scatter(
            df,
            x='Price/Unit',
            y='Monthly Revenue',
            color='Pack Type',
            title='Revenue vs. Price per Unit by Packaging Type',
            labels={'Price/Unit': 'Price per Unit', 'Monthly Revenue': 'Revenue ($)'}
        )
        scatter_revenue_price_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        scatter_revenue_price_packaging_plot_html = scatter_revenue_price_packaging_fig.to_html(full_html=False)

        # 4. Box Plot for Revenue Distribution by Packaging Type
        box_revenue_packaging_fig = px.box(
            df,
            x='Pack Type',
            y='Monthly Revenue',
            title='Revenue Distribution by Packaging Type'
        )
        box_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        box_revenue_packaging_plot_html = box_revenue_packaging_fig.to_html(full_html=False)

        # 5. Histogram for Revenue Distribution by Packaging Type
        hist_revenue_packaging_fig = px.histogram(
            df,
            x='Pack Type',
            y='Monthly Revenue',
            title='Revenue Distribution by Packaging Type',
            labels={'Pack Type': 'Packaging Type', 'Monthly Revenue': 'Revenue ($)'},
            color='Pack Type'
        )
        hist_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        hist_revenue_packaging_plot_html = hist_revenue_packaging_fig.to_html(full_html=False)

        # 6. Violin Plot for Revenue by Packaging Type
        violin_revenue_packaging_fig = px.violin(
            df,
            x='Pack Type',
            y='Monthly Revenue',
            box=True,
            title='Revenue by Packaging Type'
        )
        violin_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        violin_revenue_packaging_plot_html = violin_revenue_packaging_fig.to_html(full_html=False)

        # 7. Treemap for Revenue by Packaging Type and Product
        treemap_revenue_packaging_fig = px.treemap(
            df,
            path=['Pack Type', 'Product Name'],
            values='Monthly Revenue',
            title='Revenue by Packaging Type and Product'
        )
        treemap_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        treemap_revenue_packaging_plot_html = treemap_revenue_packaging_fig.to_html(full_html=False)

        # 8. Line Plot for Revenue Trends Over Time by Packaging Type
        line_revenue_trend_packaging_fig = px.line(
            df,
            x='Sales Month',
            y='Monthly Revenue',
            color='Pack Type',
            title='Revenue Trends Over Time by Packaging Type',
            labels={'Sales Month': 'Month', 'Monthly Revenue': 'Revenue ($)'}
        )
        line_revenue_trend_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        line_revenue_trend_packaging_plot_html = line_revenue_trend_packaging_fig.to_html(full_html=False)

        # 9. Area Plot for Cumulative Revenue by Packaging Type
        df['Cumulative Revenue'] = df.groupby('Pack Type')['Monthly Revenue'].cumsum()
        area_cumulative_revenue_packaging_fig = px.area(
            df,
            x='Sales Month',
            y='Cumulative Revenue',
            color='Pack Type',
            title='Cumulative Revenue by Packaging Type',
            labels={'Sales Month': 'Month', 'Cumulative Revenue': 'Cumulative Revenue ($)'}
        )
        area_cumulative_revenue_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        area_cumulative_revenue_packaging_plot_html = area_cumulative_revenue_packaging_fig.to_html(full_html=False)

        # 10. Density Heatmap for Revenue and Sales Volume by Packaging Type
        density_heatmap_revenue_volume_packaging_fig = px.density_heatmap(
            df,
            x='Monthly Sales Volume (units)',
            y='Monthly Revenue',
            z='Pack Type',
            title='Density Heatmap of Revenue and Sales Volume by Packaging Type',
            labels={'Monthly Sales Volume (units)': 'Sales Volume (units)', 'Monthly Revenue': 'Revenue ($)'}
        )
        density_heatmap_revenue_volume_packaging_fig.update_layout(margin=dict(l=20, r=20, t=40, b=40), height=350, width=500, title_x=0.5)
        density_heatmap_revenue_volume_packaging_plot_html = density_heatmap_revenue_volume_packaging_fig.to_html(full_html=False)

        context = {
            'bar_revenue_packaging_plot': bar_revenue_packaging_plot_html,
            'pie_revenue_packaging_plot': pie_revenue_packaging_plot_html,
            'scatter_revenue_price_packaging_plot': scatter_revenue_price_packaging_plot_html,
            'box_revenue_packaging_plot': box_revenue_packaging_plot_html,
            'hist_revenue_packaging_plot': hist_revenue_packaging_plot_html,
            'violin_revenue_packaging_plot': violin_revenue_packaging_plot_html,
            'treemap_revenue_packaging_plot': treemap_revenue_packaging_plot_html,
            'line_revenue_trend_packaging_plot': line_revenue_trend_packaging_plot_html,
            'area_cumulative_revenue_packaging_plot': area_cumulative_revenue_packaging_plot_html,
            'density_heatmap_revenue_volume_packaging_plot': density_heatmap_revenue_volume_packaging_plot_html,
        }

        return render(request, 'dashboard_app/revenue_packaging_detail.html', context)

    except Exception as e:
        print("An error occurred:", e)
        return render(request, 'dashboard_app/error.html', {'error_message': str(e)})


#####################################

def machine_learning_models_detail(request):
    # Context can include model results, summaries, metrics, etc.
    context = {
        'model_performance_summary': "This is where you would show details about your machine learning models, such as performance metrics, predictions, and insights."
    }
    return render(request, 'dashboard_app/machine_learning_models_detail.html', context)






# dashboard_app/views.py

# dashboard_app/views.py

# dashboard_app/views.py

# dashboard_app/views.py

import os
import json
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.utils.safestring import mark_safe
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder

def model_performance(request):
    json_file_path = os.path.join(settings.BASE_DIR, 'dashboard_app', 'data', 'model_performance_data.json')
    try:
        with open(json_file_path, 'r') as f:
            performances = json.load(f)
    except Exception:
        performances = []
    
    if performances:
        df = pd.DataFrame(performances)
        df['trained_at'] = pd.to_datetime(df['trained_at'])
        
        # Bar Chart for R² Scores
        fig_r2 = px.bar(
            df,
            x='model_name',
            y='r2_score',
            labels={'model_name': 'Model', 'r2_score': 'R² Score'},
            title='R² Scores of Models',
            text='r2_score'
        )
        fig_r2.update_traces(texttemplate='%{text:.2f}', textposition='auto')
        graph_r2 = json.dumps(fig_r2, cls=PlotlyJSONEncoder)
        
        # Bar Chart for MSE
        fig_mse = px.bar(
            df,
            x='model_name',
            y='mse',
            labels={'model_name': 'Model', 'mse': 'Mean Squared Error (MSE)'},
            title='MSE Scores of Models',
            text='mse'
        )
        fig_mse.update_traces(texttemplate='%{text:.2f}', textposition='auto')
        graph_mse = json.dumps(fig_mse, cls=PlotlyJSONEncoder)
        
        # Bar Chart for Accuracy within ±10%
        fig_accuracy = px.bar(
            df,
            x='model_name',
            y='accuracy_within_tolerance',
            labels={'model_name': 'Model', 'accuracy_within_tolerance': 'Accuracy within ±10%'},
            title='Accuracy within ±10% of Actual Values',
            text='accuracy_within_tolerance'
        )
        fig_accuracy.update_traces(texttemplate='%{text:.2f}%', textposition='auto')
        graph_accuracy = json.dumps(fig_accuracy, cls=PlotlyJSONEncoder)
        
        # Scatter Plot for R² vs MSE
        fig_scatter = px.scatter(
            df,
            x='r2_score',
            y='mse',
            text='model_name',
            labels={'r2_score': 'R² Score', 'mse': 'Mean Squared Error (MSE)'},
            title='R² Score vs MSE',
            hover_data={'model_name': False}
        )
        fig_scatter.update_traces(textposition='top center')
        graph_scatter = json.dumps(fig_scatter, cls=PlotlyJSONEncoder)
        
        # Line Chart for R² over Time
        fig_line = px.line(
            df,
            x='trained_at',
            y='r2_score',
            labels={'trained_at': 'Trained At', 'r2_score': 'R² Score'},
            title='R² Score Over Time',
            markers=True
        )
        graph_line = json.dumps(fig_line, cls=PlotlyJSONEncoder)
        
        # Pie Chart for Accuracy Categories
        high_accuracy = df[df['accuracy_within_tolerance'] >= 80].shape[0]
        medium_accuracy = df[(df['accuracy_within_tolerance'] >= 60) & (df['accuracy_within_tolerance'] < 80)].shape[0]
        low_accuracy = df[df['accuracy_within_tolerance'] < 60].shape[0]
        fig_pie = px.pie(
            names=['≥80%', '60-79%', '<60%'],
            values=[high_accuracy, medium_accuracy, low_accuracy],
            title='Accuracy within ±10% Categories'
        )
        graph_pie = json.dumps(fig_pie, cls=PlotlyJSONEncoder)
    else:
        graph_r2 = json.dumps({})
        graph_mse = json.dumps({})
        graph_accuracy = json.dumps({})
        graph_scatter = json.dumps({})
        graph_line = json.dumps({})
        graph_pie = json.dumps({})
    
    context = {
        'performances': performances,
        'graph_r2': graph_r2,
        'graph_mse': graph_mse,
        'graph_accuracy': graph_accuracy,
        'graph_scatter': graph_scatter,
        'graph_line': graph_line,
        'graph_pie': graph_pie,
    }
    
    return render(request, 'dashboard_app/model_performance.html', context)

