import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

def create_revenue_chart(data):
    try:
        # Filter revenue data and remove zero amounts
        revenue_data = data[
            (data['Type'] == 'Revenue') & 
            (data['Amount'] != 0) &
            (data['Level'] == 1)  # Main categories only
        ].copy()
        
        if len(revenue_data) == 0:
            return go.Figure().add_annotation(
                text="No revenue data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Sort by absolute amount
        revenue_data['AbsAmount'] = revenue_data['Amount'].abs()
        revenue_data = revenue_data.sort_values('AbsAmount', ascending=False)
        
        fig = px.bar(
            revenue_data,
            x='Account',
            y='Amount',
            title='Revenue by Category',
            color='Account',
            text='Amount'
        )
        
        fig.update_layout(
            xaxis_title="Category",
            yaxis_title="Amount (KES)",
            showlegend=True,
            xaxis_tickangle=-45,
            height=500
        )
        
        # Format the text to show currency
        fig.update_traces(
            texttemplate='KES %{text:,.0f}',
            textposition='outside'
        )
        
        return fig
    except Exception as e:
        return go.Figure().add_annotation(
            text=f"Error creating revenue chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )

def create_expense_chart(data):
    try:
        # Filter expense data
        expense_data = data[
            (data['Type'] == 'Expense') & 
            (data['Amount'] != 0) &
            (data['Level'] == 1)  # Main categories only
        ].copy()
        
        if len(expense_data) == 0:
            return go.Figure().add_annotation(
                text="No expense data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Use absolute values for the pie chart
        expense_data['Amount'] = expense_data['Amount'].abs()
        
        fig = px.pie(
            expense_data,
            values='Amount',
            names='Account',
            title='Expense Distribution by Category',
            hole=0.4
        )
        
        # Update traces to show percentages and absolute values
        fig.update_traces(
            textinfo='percent+value',
            hovertemplate="<b>%{label}</b><br>Amount: KES %{value:,.0f}<br>Percentage: %{percent}<extra></extra>"
        )
        
        fig.update_layout(height=500)
        
        return fig
    except Exception as e:
        return go.Figure().add_annotation(
            text=f"Error creating expense chart: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )

def create_category_breakdown(data, category_type='Expense'):
    try:
        # Filter data by type and remove zero amounts
        category_data = data[
            (data['Type'] == category_type) & 
            (data['Amount'] != 0) &
            (data['Level'].isin([1, 2]))  # Include first two levels
        ].copy()
        
        if len(category_data) == 0:
            return go.Figure().add_annotation(
                text=f"No {category_type.lower()} data available",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False
            )
        
        # Sort by absolute amount
        category_data['AbsAmount'] = category_data['Amount'].abs()
        category_data = category_data.sort_values('AbsAmount', ascending=True)
        
        # Create color mapping for levels
        category_data['Level'] = category_data['Level'].map({1: 'Main Category', 2: 'Subcategory'})
        
        fig = px.bar(
            category_data,
            x='Amount',
            y='Account',
            orientation='h',
            title=f'{category_type} Breakdown by Category',
            color='Level',
            text='Amount',
            color_discrete_map={'Main Category': '#1f77b4', 'Subcategory': '#ff7f0e'}
        )
        
        fig.update_layout(
            xaxis_title="Amount (KES)",
            yaxis_title="Category",
            showlegend=True,
            height=max(400, len(category_data) * 30),  # Adjust height based on number of categories
            yaxis={'categoryorder': 'total ascending'}  # Sort bars by value
        )
        
        # Format the text to show currency
        fig.update_traces(
            texttemplate='KES %{text:,.0f}',
            textposition='outside'
        )
        
        return fig
    except Exception as e:
        return go.Figure().add_annotation(
            text=f"Error creating category breakdown: {str(e)}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )