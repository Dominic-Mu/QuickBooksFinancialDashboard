import streamlit as st
import pandas as pd
from data_processor import DataProcessor
from visualizations import create_revenue_chart, create_expense_chart, create_category_breakdown
from utils import format_kes

# Page configuration
st.set_page_config(
    page_title="QuickBooks Financial Dashboard",
    page_icon="💰",
    layout="wide"
)

class FinancialDashboard:
    def __init__(self):
        self.data_processor = DataProcessor()
        
    def setup_sidebar(self):
        st.sidebar.title("Dashboard Controls")
        
        # File upload section
        st.sidebar.subheader("Data Import")
        uploaded_files = st.sidebar.file_uploader(
            "Upload QuickBooks Reports (CSV)",
            type=['csv'],
            accept_multiple_files=True,
            help="Upload both Profit & Loss and Balance Sheet reports"
        )
        
        if uploaded_files:
            for file in uploaded_files:
                self.data_processor.process_file(file)
            
        # Filtering section
        st.sidebar.subheader("Filters")
        if self.data_processor.data is not None:
            # Account level filter
            level_filter = st.sidebar.selectbox(
                "Account Detail Level",
                options=[1, 2, 3],
                index=0,  # Default to first option
                help="1: Main categories, 2: Subcategories, 3: Detailed accounts"
            )
            
            # Account type filter
            account_types = ['All'] + list(self.data_processor.data['Type'].unique())
            account_type = st.sidebar.selectbox(
                "Account Type",
                options=account_types,
                index=0  # Default to 'All'
            )
            
            return level_filter, account_type
        return None, None

    def render_dashboard(self):
        st.title("QuickBooks Financial Dashboard")
        
        level_filter, account_type = self.setup_sidebar()
        
        if self.data_processor.data is None:
            st.info("Please upload QuickBooks report files (Profit & Loss and/or Balance Sheet) to begin.")
            return
            
        # Financial Overview section
        st.header("Financial Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_revenue = self.data_processor.get_total_revenue()
            st.metric("Total Revenue", format_kes(total_revenue))
            
        with col2:
            total_expenses = self.data_processor.get_total_expenses()
            st.metric("Total Expenses", format_kes(total_expenses))
            
        with col3:
            net_profit = total_revenue - total_expenses
            st.metric(
                "Net Profit",
                format_kes(net_profit),
                delta=f"{(net_profit/total_revenue*100 if total_revenue else 0):.1f}%"
            )
            
        with col4:
            profit_margin = (net_profit / total_revenue * 100) if total_revenue else 0
            st.metric("Profit Margin", f"{profit_margin:.1f}%")
        
        # Charts section
        st.header("Financial Analysis")
        
        # Revenue Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Revenue Breakdown")
            revenue_chart = create_revenue_chart(self.data_processor.data)
            st.plotly_chart(revenue_chart, use_container_width=True)
        
        with col2:
            st.subheader("Expense Distribution")
            expense_chart = create_expense_chart(self.data_processor.data)
            st.plotly_chart(expense_chart, use_container_width=True)
        
        # Detailed Breakdown
        st.header("Detailed Account Breakdown")
        tab1, tab2 = st.tabs(["Revenue Accounts", "Expense Accounts"])
        
        with tab1:
            revenue_breakdown = create_category_breakdown(
                self.data_processor.data,
                category_type='Revenue'
            )
            st.plotly_chart(revenue_breakdown, use_container_width=True)
            
        with tab2:
            expense_breakdown = create_category_breakdown(
                self.data_processor.data,
                category_type='Expense'
            )
            st.plotly_chart(expense_breakdown, use_container_width=True)
        
        # Data Export section
        st.header("Export Data")
        if st.button("Download Processed Data"):
            csv = self.data_processor.data.to_csv(index=False)
            st.download_button(
                label="Click to Download CSV",
                data=csv,
                file_name="financial_data.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    dashboard = FinancialDashboard()
    dashboard.render_dashboard()