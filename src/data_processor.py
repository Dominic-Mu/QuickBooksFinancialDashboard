import pandas as pd
import streamlit as st
from pathlib import Path
import numpy as np

class DataProcessor:
    def __init__(self):
        self.data = None
        self.balance_sheet = None
        self.profit_loss = None
        
    def process_file(self, file):
        try:
            # Determine file type from name
            filename = file.name.lower()
            
            # Read the CSV file
            df = pd.read_csv(file)
            
            # Clean column names
            df.columns = [col.strip() if isinstance(col, str) else col for col in df.columns]
            
            # Standardize column names
            column_mapping = {
                'Account Type': 'AccountType',
                'Account_Type': 'AccountType',
                'AccountType': 'AccountType',
                'Account': 'Account',
                'Debit': 'Debit',
                'Credit': 'Credit'
            }
            df = df.rename(columns=column_mapping)
            
            if 'profitandloss' in filename:
                self._process_profit_loss(df)
            elif 'balancesheet' in filename:
                self._process_balance_sheet(df)
            
            # Combine data if both files are loaded
            self._combine_data()
            
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")
            self.data = None
    
    def _process_profit_loss(self, df):
        try:
            # Remove empty rows and reset index
            df = df.dropna(how='all').reset_index(drop=True)
            
            # Calculate amount from Debit and Credit columns
            df['Amount'] = pd.to_numeric(df['Credit'].fillna(0), errors='coerce') - pd.to_numeric(df['Debit'].fillna(0), errors='coerce')
            
            # Clean the Account column
            df['Account'] = df['Account'].fillna('Uncategorized')
            
            # Determine hierarchy level from Account structure
            df['Level'] = df['Account'].apply(self._determine_level_from_account)
            
            # Convert date
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            
            # Use AccountType for classification
            df['Type'] = df['AccountType'].apply(self._standardize_account_type)
            
            # Clean and structure the data
            self.profit_loss = df[
                ['Date', 'Account', 'Amount', 'Type', 'Level', 'AccountType']
            ].copy()
            
            # Scale down large numbers
            self.profit_loss['Amount'] = self.profit_loss['Amount'] / 1000  # Convert to thousands
            
        except Exception as e:
            st.error(f"Error processing Profit & Loss data: {str(e)}")
            self.profit_loss = None
    
    def _process_balance_sheet(self, df):
        try:
            # Remove empty rows and reset index
            df = df.dropna(how='all').reset_index(drop=True)
            
            # Calculate amount from Debit and Credit columns
            df['Amount'] = pd.to_numeric(df['Credit'].fillna(0), errors='coerce') - pd.to_numeric(df['Debit'].fillna(0), errors='coerce')
            
            # Clean the Account column
            df['Account'] = df['Account'].fillna('Uncategorized')
            
            # Determine hierarchy level from Account structure
            df['Level'] = df['Account'].apply(self._determine_level_from_account)
            
            # Convert date
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            
            # Use AccountType for classification
            df['Type'] = df['AccountType'].apply(self._standardize_account_type)
            
            # Clean and structure the data
            self.balance_sheet = df[
                ['Date', 'Account', 'Amount', 'Type', 'Level', 'AccountType']
            ].copy()
            
            # Scale down large numbers
            self.balance_sheet['Amount'] = self.balance_sheet['Amount'] / 1000  # Convert to thousands
            
        except Exception as e:
            st.error(f"Error processing Balance Sheet data: {str(e)}")
            self.balance_sheet = None
    
    def _determine_level_from_account(self, account):
        if pd.isna(account):
            return 1
        # Count the number of ':' to determine level
        return account.count(':') + 1
    
    def _standardize_account_type(self, account_type):
        if pd.isna(account_type):
            return 'Other'
            
        account_type = str(account_type).lower().strip()
        
        # Map account types to standard categories
        if any(word in account_type for word in ['income', 'revenue', 'sales']):
            return 'Revenue'
        elif any(word in account_type for word in ['expense', 'cost', 'expenditure']):
            return 'Expense'
        elif any(word in account_type for word in ['asset', 'bank', 'cash']):
            return 'Asset'
        elif any(word in account_type for word in ['liability', 'loan', 'payable']):
            return 'Liability'
        elif any(word in account_type for word in ['equity', 'capital']):
            return 'Equity'
        else:
            return 'Other'
    
    def _combine_data(self):
        if self.profit_loss is not None:
            self.data = self.profit_loss.copy()
        
        if self.balance_sheet is not None:
            if self.data is None:
                self.data = self.balance_sheet.copy()
            else:
                self.data = pd.concat([self.data, self.balance_sheet], ignore_index=True)
        
        if self.data is not None:
            # Ensure all required columns exist
            required_columns = ['Account', 'Amount', 'Type', 'Level', 'Date']
            for col in required_columns:
                if col not in self.data.columns:
                    self.data[col] = None
    
    def get_total_revenue(self):
        if self.data is None:
            return 0
        return abs(self.data[self.data['Type'] == 'Revenue']['Amount'].sum())
    
    def get_total_expenses(self):
        if self.data is None:
            return 0
        return abs(self.data[self.data['Type'] == 'Expense']['Amount'].sum())
    
    def filter_data(self, level=None, account_type=None):
        if self.data is None:
            return None
            
        filtered_data = self.data.copy()
        
        if level is not None:
            filtered_data = filtered_data[filtered_data['Level'] == level]
            
        if account_type and account_type != 'All':
            filtered_data = filtered_data[filtered_data['Type'] == account_type]
            
        return filtered_data